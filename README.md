# Monitor Inteligente PS

Sistema para monitorar pacientes do Painel PS, consultar exames laboratoriais no Hemolabor e exames de imagem no Clinux.

## Rodar

```powershell
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
python -m playwright install chromium

$env:HEMO_LOGIN="rlc"
$env:HEMO_SENHA="hemo2016"
$env:CLINUX_LOGIN="Dicomvix"
$env:CLINUX_SENHA="imagem"

python app.py
```

Acesse:

```text
http://127.0.0.1:5055
```
