import excel
import request_operations as ro

# Create Virtual Environment        >python3 -m venv .venv
# Activate Virtual Environment      >source .venv/bin/activate
# Install a package into the Env    >python3 -m pip install openpyxl
# De-activate Virtual Environment   >deactivate

msg = "hola mundo"
print(msg)

kariyer_jobads = excel.read_kariyer_jobads()
f3 = kariyer_jobads[:3]
print(f3)



ro.time_to_first_byte()


