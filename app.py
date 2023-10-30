from flask import Flask, render_template, request, redirect, send_file
import numpy as np
from keras.models import load_model
from joblib import load

app = Flask(__name__)

symptoms_spanish = [(0, 'debilidad de un lado del cuerpo'),
                    (1, 'dolor de cuello'),
                    (2, 'náuseas'),
                    (3, 'visión borrosa y distorsionada'),
                    (4, 'sensorio alterado'),
                    (5, 'debilidad en las extremidades'),
                    (6, 'manchas descoloridas'),
                    (7, 'mareo'),
                    (8, 'hemorragia estomacal'),
                    (9, 'rigidez en el cuello'),
                    (10, 'uñas inflamadas'),
                    (11, 'hinchazón en las articulaciones'),
                    (12, 'dolor en las articulaciones'),
                    (13, 'úlceras en la lengua'),
                    (14, 'historial de consumo de alcohol'),
                    (15, 'cambios de humor'),
                    (16, 'escalofríos'),
                    (17, 'vasos sanguíneos hinchados'),
                    (18, 'sudoración'),
                    (19, 'depresión'),
                    (20, 'dolor de espalda'),
                    (21, 'obesidad'),
                    (22, 'debilitamiento muscular'),
                    (23, 'falta de aliento'),
                    (24, 'aumento del apetito'),
                    (25, 'movimientos giratorios'),
                    (26, 'olor desagradable en la orina'),
                    (27, 'desHidratación'),
                    (28, 'picazón'),
                    (29, 'dolor abdominal'),
                    (30, 'estreñimiento'),
                    (31, 'micción ardiente'),
                    (32, 'heces sanguinolentas'),
                    (33, 'ritmo cardíaco rápido'),
                    (34, 'picazón interna'),
                    (35, 'caminar doloroso'),
                    (36, 'poliuria'),
                    (37, 'acidez'),
                    (38, 'fatiga'),
                    (39, 'fiebre leve'),
                    (40, 'manchas en la garganta'),
                    (41, 'orina oscura'),
                    (42, 'apariencia tóxica (tifos)'),
                    (43, 'manos y pies fríos'),
                    (44, 'llagas rojas alrededor de la nariz'),
                    (45, 'irritabilidad'),
                    (46, 'rigidez en el movimiento'),
                    (47, 'descamación de la piel'),
                    (48, 'espinillas llenas de pus'),
                    (49, 'color amarillo en los ojos'),
                    (50, 'erupciones cutáneas nodales'),
                    (51, 'uñas quebradizas'),
                    (52, 'cara y ojos hinchados'),
                    (53, 'niveles irregulares de azúcar'),
                    (54, 'aumento de peso'),
                    (55, 'diarrea'),
                    (56, 'sangre en el esputo'),
                    (57, 'habla arrastrada'),
                    (58, 'trastornos visuales'),
                    (59, 'ganglios linfáticos hinchados'),
                    (60, 'malestar'),
                    (61, 'moretones'),
                    (62, 'sobrecarga de líquidos'),
                    (63, 'inestabilidad'),
                    (64, 'tiroides agrandada'),
                    (65, 'letargo'),
                    (66, 'venas prominentes en la pantorrilla'),
                    (67, 'vómitos'),
                    (68, 'inyecciones no estériles'),
                    (69, 'distensión abdominal'),
                    (70, 'irritación en el ano'),
                    (71, 'puntos negros'),
                    (72, 'escalofríos'),
                    (73, 'costras amarillas supurantes'),
                    (74, 'orina amarilla'),
                    (75, 'liberación de gases'),
                    (76, 'dolor muscular'),
                    (77, 'sensación continua de orina'),
                    (78, 'polvo parecido a la plata'),
                    (79, 'palpitaciones'),
                    (80, 'dolor en la región anal'),
                    (81, 'pequeñas muescas en las uñas'),
                    (82, 'piel amarillenta'),
                    (83, 'pérdida de equilibrio'),
                    (84, 'contactos extramatrimoniales'),
                    (85, 'coma'),
                    (86, 'ansiedad'),
                    (87, 'dolor abdominal'),
                    (88, 'ampolla'),
                    (89, 'dolor de estómago'),
                    (90, 'dolor durante las evacuaciones intestinales'),
                    (91, 'lagrimeo de los ojos'),
                    (92, 'esputo oxidado'),
                    (93, 'presión en los senos paranasales'),
                    (94, 'hinchazón del estómago'),
                    (95, 'historial familiar'),
                    (96, 'indigestión'),
                    (97, 'extremidades hinchadas'),
                    (98, 'piernas hinchadas'),
                    (99, 'erupción cutánea'),
                    (100, 'enrojecimiento de los ojos'),
                    (101, 'menstruación anormal'),
                    (102, 'calambres'),
                    (103, 'insuficiencia hepática aguda'),
                    (104, 'tos'),
                    (105, 'recepción de transfusión de sangre'),
                    (106, 'pérdida de apetito'),
                    (107, 'dolor en el pecho'),
                    (108, 'estornudos continuos'),
                    (109, 'ojos hundidos'),
                    (110, 'irritación de garganta'),
                    (111, 'dolor en las rodillas'),
                    (112, 'manchas rojas en el cuerpo'),
                    (113, 'pérdida de peso'),
                    (114, 'hambre excesiva'),
                    (115, 'labios secos y hormigueantes'),
                    (116, 'escoriación'),
                    (117, 'fiebre alta'),
                    (118, 'congestión'),
                    (119, 'dolor en la cadera'),
                    (120, 'dolor de cabeza'),
                    (121, 'pérdida del olfato'),
                    (122, 'flema'),
                    (123, 'inquietud'),
                    (124, 'manchado durante la micción'),
                    (125, 'dolor detrás de los ojos'),
                    (126, 'debilidad muscular'),
                    (127, 'malestar en la vejiga'),
                    (128, 'falta de concentración'),
                    (129, 'rinorrea'),
                    (130, 'esputo mucoso')]

@app.route('/')
def hello_world():  # put application's code here
    return render_template('index.html', symptoms_spanish=symptoms_spanish)


@app.route('/symptoms', methods=['POST'])
def symptoms():
    if request.method == 'POST':
        symptoms = request.get_json()
        model_transform = load('pca.joblib')
        encoder = load('disease_encoder.joblib')

        row_data_reshaped = np.array(symptoms).reshape(1, -1)
        x = model_transform.transform(row_data_reshaped)
        model = load_model('model.keras')
        prediction = model.predict(x)
        predicted_class = np.argmax(prediction)
        print(predicted_class)
        index = predicted_class
        issues = encoder.inverse_transform([index])
        return list(issues)[0]


if __name__ == '__main__':
    app.run()
