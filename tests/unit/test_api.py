def test_json_data_empty(client):
    response = client.post("/backend/challenge", json={})
    assert response.status_code == 400


def test_json_data_invalid(client):
    data = {"vehicles": []}
    response = client.post("/backend/challenge", json=data)
    assert response.status_code == 400


def test_json_data_valid(client):
    data = {
        "vehicles": [
            {
                "features": [
                    {"description": {"short": "5.2 Liter V8"}, "feature": "ENGINE"},
                    {"description": {"short": '19" Felgen'}, "feature": "RIM"},
                    {
                        "description": {"short": "Service bei " "120.000 km"},
                        "feature": "SERVICE",
                    },
                    {
                        "description": {
                            "long": "Kein Kratzer im " "Lack, " "Scheckheftgepflegt, " "Garagenwagen, von " "ner alten Oma " "gefahren",
                            "short": "Top Zustand",
                        },
                        "feature": "INFO",
                    },
                ],
                "id": "VIN1",
            },
            {
                "features": [
                    {"description": {"short": "1.8 Liter V6"}, "feature": "ENGINE"},
                    {"description": {"short": "Pirelli P7"}, "feature": "WHEEL"},
                    {
                        "description": {"short": "Service bei " "80.000 km"},
                        "feature": "SERVICE",
                    },
                ],
                "id": "VIN2",
            },
        ]
    }

    response = client.post("/backend/challenge", json=data)
    assert response.status_code == 200

    # TODO clean up the files or use pyfakefs
