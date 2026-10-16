import math

import numpy as np

try:
    import face_recognition
except ImportError:  # pragma: no cover - optional for local demo builds
    face_recognition = None

from .models import FaceEmbedding, FaceImage


RECOGNITION_THRESHOLD = 0.45


class EnrollmentError(Exception):
    pass


def enroll_face_image(student, image_file, angle_label):
    if face_recognition is None:
        raise EnrollmentError('Face recognition library is not installed in this environment.')
    if image_file is None:
        raise EnrollmentError('Please upload a valid photo.')

    face_image = FaceImage.objects.create(student=student, image=image_file, angle_label=angle_label)
    try:
        loaded_image = face_recognition.load_image_file(face_image.image.path)
        face_locations = face_recognition.face_locations(loaded_image, model='hog')
        if len(face_locations) == 0:
            raise EnrollmentError('No face detected in this photo. Please retake it with better lighting.')
        if len(face_locations) > 1:
            raise EnrollmentError('Multiple faces detected. Enrollment photos must contain only the student.')

        top, right, bottom, left = face_locations[0]
        face_width = right - left
        if face_width < 112:
            raise EnrollmentError('Face is too small in the frame. Move closer to the camera.')

        encodings = face_recognition.face_encodings(loaded_image, known_face_locations=face_locations)
        if not encodings:
            raise EnrollmentError('The system could not generate a face encoding from this image.')

        FaceEmbedding.objects.create(
            student=student,
            source_image=face_image,
            vector=encodings[0].tolist(),
            model_version='v1',
        )
        return True
    except EnrollmentError:
        face_image.delete()
        raise
    except Exception:
        face_image.delete()
        raise EnrollmentError('The uploaded image could not be processed.')


def recognize_classroom_photo(image_path):
    if face_recognition is None:
        return []

    loaded_image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(loaded_image, model='hog')
    face_encodings = face_recognition.face_encodings(loaded_image, known_face_locations=face_locations)

    all_embeddings = list(FaceEmbedding.objects.filter(is_active=True).select_related('student'))
    if not all_embeddings:
        return [
            {'location': loc, 'student': None, 'confidence': 0.0, 'status': 'UNKNOWN'}
            for loc in face_locations
        ]

    known_vectors = np.array([embedding.vector for embedding in all_embeddings], dtype=float)
    known_students = [embedding.student for embedding in all_embeddings]
    results = []
    matched_student_ids = set()

    for location, face_vector in zip(face_locations, face_encodings):
        distances = np.linalg.norm(known_vectors - face_vector, axis=1)
        best_index = int(np.argmin(distances))
        best_distance = float(distances[best_index])
        if best_distance <= RECOGNITION_THRESHOLD:
            candidate = known_students[best_index]
            confidence = round(1 - best_distance, 3)
            if candidate.id in matched_student_ids:
                results.append({'location': location, 'student': candidate, 'confidence': confidence, 'status': 'DUPLICATE_REVIEW'})
            else:
                matched_student_ids.add(candidate.id)
                results.append({'location': location, 'student': candidate, 'confidence': confidence, 'status': 'MATCHED'})
        else:
            results.append({'location': location, 'student': None, 'confidence': round(1 - best_distance, 3), 'status': 'UNKNOWN'})

    return results
