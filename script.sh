#!/bin/bash

# Configuration
BASE_URL="http://localhost:8000/api/"
LOGIN_ENDPOINT="login/"  # Update with your actual login endpoint
REGISTER_ENDPOINT="register/"  # Update with your actual registration endpoint

ADMIN_USERNAME="admin"  # Replace with admin username
ADMIN_PASSWORD="pass"  # Replace with admin password

# Login and get the access token
response=$(curl -s -X POST "$BASE_URL$LOGIN_ENDPOINT" -d "username=$ADMIN_USERNAME&password=$ADMIN_PASSWORD&requested_role=admin")
echo $response
ACCESS_TOKEN=$(echo $response | jq -r '.access')

echo "Access token received: $ACCESS_TOKEN"

# Register 3 mentors
for i in {1..3}; do
    MENTOR_USERNAME="mentor$i"
    MENTOR_EMAIL="mentor$i@example.com"
    MENTOR_PASSWORD="mentor${i}pass"
    MENTOR_NAME="Mentor $i"
    MENTOR_BRANCH="Branch$i"
    MENTOR_CONTACT="12345678$i"

    curl -s -X POST "$BASE_URL$REGISTER_ENDPOINT" \
         -H "Authorization: Bearer $ACCESS_TOKEN" \
         -d "username=$MENTOR_USERNAME&email=$MENTOR_EMAIL&password=$MENTOR_PASSWORD&password_confirm=$MENTOR_PASSWORD&name=$MENTOR_NAME&branch=$MENTOR_BRANCH&contact=$MENTOR_CONTACT&role=mentor"
    echo
done

# Register 3 students for each mentor
for i in {1..3}; do
    for j in {1..3}; do
        STUDENT_USERNAME="student${i}_${j}"
        STUDENT_EMAIL="student${i}_${j}@example.com"
        STUDENT_PASSWORD="student${i}_${j}pass"
        STUDENT_NAME="Student $j"
        STUDENT_BRANCH="SMentorBranch$i"
        STUDENT_CONTACT="22345678$j"
        MENTOR_USERNAME="mentor$i"

        curl -s -X POST "$BASE_URL$REGISTER_ENDPOINT" \
             -H "Authorization: Bearer $ACCESS_TOKEN" \
             -d "sem=5&username=$STUDENT_USERNAME&email=$STUDENT_EMAIL&password=$STUDENT_PASSWORD&password_confirm=$STUDENT_PASSWORD&name=$STUDENT_NAME&branch=$STUDENT_BRANCH&contact=$STUDENT_CONTACT&role=student&mid=$MENTOR_USERNAME"

        echo
    done
done

echo "All registrations completed."

#GET request to get list of all students
curl -X GET http://localhost:8000/api/students/ \
     -H "Authorization: Bearer $ACCESS_TOKEN" \

#GET request to get list of all mentors
curl -X GET http://localhost:8000/api/mentors/ \
     -H "Authorization: Bearer $ACCESS_TOKEN" \

# PATCH request to change student data. Replace {id} by the id from GET students
curl -X PATCH http://localhost:8000/api/students/{id} \
     -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name": "New StudName","branch":"SomeBranch","email": "newemail@example.com","sem" : "6", "mid":"mentor2"}'

curl -X PATCH http://localhost:8000/api/students/ \
     -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '[
          {"id": id1, "name": "New Name 1", "branch": "SomeBranch", "email": "newemail1@example.com", "sem": "6", "mid": "mentor2"},
          {"id": id2, "name": "New StudenName 2", "branch": "AnotherBranch", "email": "newemail2@example.com", "sem": "5", "mid": "mentor3"}
     ]'

#PATCH request to change mentor data. Replace {id} by the id from GET mentors
curl -X PATCH http://localhost:8000/api/mentors/{id}/ \
     -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '{"name": "New Student Name","branch":"NewBranch","email": "newemail@example.com", "mid":"mentor2", "contact":"2345678901"}'

curl -X PATCH http://localhost:8000/api/mentors/ \
     -H "Authorization: Bearer $ACCESS_TOKEN" \
     -H "Content-Type: application/json" \
     -d '[
          {"id": id1, "name": "New Name 1", "branch": "Branch1", "email": "newemail1@example.com"},
          {"id": id2, "name": "New Name 2", "branch": "Branch2", "email": "newemail2@example.com"}
     ]'