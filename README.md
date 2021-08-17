Необхідні залежності :

torch
torchaudio
omegaconf
glob
zipfile
tensorflow
tensorflow.keras
numpy
flask-restful
flask


Для запуску сервера перейдіть в кореневу папку і пропишіть комаду sudo python3 app.py.

Щоб відправити POST/PUT запит відкрийте новий термінал і пропишіть команду (як приклад):
 curl -X POST 127.0.0.1:5000/classified_audios/1 -H 'Content-Type: application/json' -d '{"filepath":"audios/record.wav"}' | jq

 jq - для того щоб не було проблем з кирилицею


P.S.
 Деякі очевидні заперечувальні аудіо-відповіді можуть неправильно класифікуватись, це зв'язано з малим датасетом, а також з можливим перенавчанням