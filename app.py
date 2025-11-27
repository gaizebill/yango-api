import streamlit as st
import requests
import json
import os
import time


st.set_page_config(page_title="Yango API Playground", page_icon="🚚", layout="wide")

st.title("Yango B2B API Playground")
st.write("Interfaz simple para probar los endpoints de Yango B2B sin CORS y sin necesidad de Postman.")

# Leer token desde variable de entorno
YANGO_TOKEN = os.getenv("YANGO_TOKEN")

if not YANGO_TOKEN:
    st.error("ERROR: No existe la variable de entorno YANGO_TOKEN. Configúrala en tu terminal.")
    st.stop()

st.sidebar.header("Endpoints disponibles")
endpoint = st.sidebar.selectbox(
    "Selecciona un endpoint",
    [
        "/tariffs",
        "/check-price",
        "/claims/create"
    ]
)

BASE_URL = "https://b2b.taxi.yandex.net/b2b/cargo/integration/v2"

default_bodies = {
    "/tariffs": {
        "start_point": [-63.19693640595825, -17.757501746861674]
    },
    "/check-price": {
        "items": [
            {
                "title": "Item sample",
                "cost_currency": "BOB",
                "size": {"width": 10, "height": 10, "length": 10},
                "weight_kg": 1
            }
        ],
        "route_points": [
            {"address": {"coordinates": [-63.19, -17.75]}},
            {"address": {"coordinates": [-63.20, -17.76]}}
        ]
    },
    "/claims/create": {
        "callback_properties": {
            "callback_url": "https://webhook.site/96fdb694-445b-4f8a-90de-93feea1388f4"
        },
        "client_requirements": {
            "taxi_class": "courier"
        },
        "comment": "Comentario",
        "emergency_contact": {
            "name": "Bill (Contacto de Emergencia)",
            "phone": "+56933418970"
        },
        "items": [
            {
                "cost_currency": "BOB",
                "cost_value": "100",
                "droppof_point": 2,
                "extra_id": "TEST-ORDER-1",
                "pickup_point": 1,
                "quantity": 1,
                "size": {
                    "height": 0.1,
                    "length": 0.1,
                    "width": 0.1
                },
                "title": "MEJOR ARTÍCULO DE PRUEBA",
                "weight": 2
            }
        ],
        "optional_return": False,
        "referral_source": "NOMBRE_DE_TU_EMPRESA",
        "route_points": [
            {
                "address": {
                    "fullname": "Cuarto Anillo, Radial 21 y, Santa Cruz de la Sierra, Bolivia",
                    "coordinates": [-63.21628097602036, -17.77781901325718],
                    "city": "Santa Cruz de la Sierra",
                    "comment": "Comentario para el repartidor",
                    "country": "Bolivia"
                },
                "contact": {
                    "email": "gaizebill@yango.com",
                    "name": "Bill (Punto A)",
                    "phone": "+56933418970"
                },
                "external_order_id": "TEST-ORDER-1",
                "point_id": 1,
                "skip_confirmation": True,
                "type": "source",
                "visit_order": 1
            },
            {
                "address": {
                    "fullname": "Av. Argentina 280, Santa Cruz de la Sierra, Bolivia",
                    "coordinates": [-63.17492724068364, -17.797046545189804],
                    "city": "Santa Cruz de la Sierra",
                    "comment": "Comentario para el repartidor en el Punto B, tal vez comentario del cliente",
                    "country": "Bolivia"
                },
                "contact": {
                    "email": "gaizebill@yango.com",
                    "name": "Bill (Punto B)",
                    "phone": "+56933418970"
                },
                "external_order_id": "TEST-ORDER-1",
                "point_id": 2,
                "skip_confirmation": True,
                "type": "destination",
                "visit_order": 2
            }
        ],
        "skip_act": False,
        "skip_client_notify": False,
        "skip_door_to_door": False,
        "skip_emergency_notify": False
    }
}

st.subheader("Request Body JSON")
body_text = st.text_area(
    "Edita el JSON:",
    json.dumps(default_bodies[endpoint], indent=2),
    height=350
)

if st.button("Enviar Request"):
    try:
        body = json.loads(body_text)

        headers = {
            "Authorization": f"Bearer {YANGO_TOKEN}",
            "Content-Type": "application/json",
            "Accept-Language": "es"
        }

        request_id = "req-" + str(int(time.time()))
        url = f"{BASE_URL}{endpoint}?request_id={request_id}"

        response = requests.post(url, headers=headers, json=body)

        st.subheader("Status Code")
        st.code(response.status_code)

        st.subheader("Response Body")
        st.code(response.text)

    except Exception as e:
        st.error(str(e))
