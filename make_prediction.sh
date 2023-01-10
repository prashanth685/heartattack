#!/usr/bin/env bash
PORT=8080
echo "Port: $PORT"

# POST method predict
curl -d '{
    "age":{
        "0":49
    },
    "sex":{
        "0":"Male"
    },
    "cp":{
        "0":"Non-anginal pain"
    },
    "trestbps":{
        "0":118
    },
    "chol":{
        "0":149
    },
    "fbs":{
        "0":"<120 mg/dl"
    },
    "restecg":{
        "0":"Left ventricular hypertrophy"
    },
    "thalach":{
        "0": 126
    },
    "exang":{
        "0":"No"
    },
    "oldpeak":{
        "0":0.8
    },
    "slope":{
        "0":"Upsloping"
    },
    "ca":{
        "0":3
    },
    "thal":{
        "0":"Normal"
    }
}'\
     -H "Content-Type: application/json" \
     -X POST http://localhost:$PORT/predict