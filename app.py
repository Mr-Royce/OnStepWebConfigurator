# app.py
from flask import Flask, render_template, request, send_file, Response
from config_generator import generate_config
import json
import io

app = Flask(__name__)

# Default configuration values (mirroring your Tkinter defaults)
default_config = {
    "PINMAP": "BTT_SKR_PRO",
    "SERIAL_A_BAUD_DEFAULT": "9600",
    "SERIAL_B_BAUD_DEFAULT": "230400",
    "SERIAL_B_ESP_FLASHING": "ON",
    "SERIAL_C_BAUD_DEFAULT": "OFF",
    "SERIAL_D_BAUD_DEFAULT": "OFF",
    "SERIAL_E_BAUD_DEFAULT": "OFF",
    "SERIAL_RADIO": "OFF",
    "WIFI_MODULE": "CH_PD",
    "STATUS_LED": "ON",
    "RETICLE_LED_DEFAULT": "OFF",
    "RETICLE_LED_MEMORY": "OFF",
    "RETICLE_LED_INVERT": "OFF",
    "WEATHER": "OFF",
    "STEP_WAVE_FORM": "PULSE",
    "NV_DRIVER": "NV_AT24C32",
    "AXIS1_DRIVER_MODEL": "TMC2130",
    "AXIS1_STEPS_PER_DEGREE": "24888",
    "AXIS1_LIMIT_MIN": "-180",
    "AXIS1_LIMIT_MAX": "180",
    "AXIS1_DRIVER_MICROSTEPS": "16",
    "AXIS1_DRIVER_MICROSTEPS_GOTO": "1",
    "AXIS1_DRIVER_IHOLD": "500",
    "AXIS1_DRIVER_IRUN": "800",
    "AXIS1_DRIVER_IGOTO": "1200",
    "AXIS1_REVERSE": "OFF",
    "AXIS1_POWER_DOWN": "OFF",
    "AXIS1_SENSE_HOME": "OFF",
    "AXIS1_DRIVER_STATUS": "ON",
    "AXIS1_DRIVER_DECAY": "OFF",
    "AXIS1_DRIVER_DECAY_GOTO": "OFF",
    "AXIS1_SENSE_LIMIT_MIN": "LIMIT_SENSE",
    "AXIS1_SENSE_LIMIT_MAX": "LIMIT_SENSE",
    "AXIS2_DRIVER_MODEL": "TMC2130",
    "AXIS2_STEPS_PER_DEGREE": "24888",
    "AXIS2_LIMIT_MIN": "-90",
    "AXIS2_LIMIT_MAX": "90",
    "AXIS2_DRIVER_MICROSTEPS": "16",
    "AXIS2_DRIVER_MICROSTEPS_GOTO": "1",
    "AXIS2_DRIVER_IHOLD": "500",
    "AXIS2_DRIVER_IRUN": "800",
    "AXIS2_DRIVER_IGOTO": "1200",
    "AXIS2_REVERSE": "OFF",
    "AXIS2_POWER_DOWN": "OFF",
    "AXIS2_SENSE_HOME": "OFF",
    "AXIS2_DRIVER_STATUS": "ON",
    "AXIS2_DRIVER_DECAY": "OFF",
    "AXIS2_DRIVER_DECAY_GOTO": "OFF",
    "AXIS2_SENSE_LIMIT_MIN": "LIMIT_SENSE",
    "AXIS2_SENSE_LIMIT_MAX": "LIMIT_SENSE",
    "MOUNT_TYPE": "GEM",
    "MOUNT_COORDS": "TOPOCENTRIC",
    "MOUNT_COORDS_MEMORY": "OFF",
    "MOUNT_ENABLE_IN_STANDBY": "OFF",
    "TIME_LOCATION_SOURCE": "DS3231",
    "TIME_LOCATION_PPS_SENSE": "HIGH",
    "STATUS_MOUNT_LED": "OFF",
    "STATUS_BUZZER": "OFF",
    "STATUS_BUZZER_DEFAULT": "OFF",
    "STATUS_BUZZER_MEMORY": "OFF",
    "ST4_INTERFACE": "OFF",
    "ST4_HAND_CONTROL": "ON",
    "ST4_HAND_CONTROL_FOCUSER": "ON",
    "GUIDE_TIME_LIMIT": "10",
    "GUIDE_DISABLE_BACKLASH": "OFF",
    "LIMIT_SENSE": "OFF",
    "LIMIT_STRICT": "OFF",
    "PARK_SENSE": "OFF",
    "PARK_SIGNAL": "OFF",
    "PARK_STATUS": "OFF",
    "PARK_STRICT": "OFF",
    "PEC_STEPS_PER_WORM_ROTATION": "0",
    "PEC_SENSE": "OFF",
    "PEC_BUFFER_SIZE_LIMIT": "720",
    "TRACK_BACKLASH_RATE": "2",
    "TRACK_AUTOSTART": "OFF",
    "TRACK_COMPENSATION_DEFAULT": "OFF",
    "TRACK_COMPENSATION_MEMORY": "OFF",
    "SLEW_RATE_BASE_DESIRED": "1",
    "SLEW_RATE_MEMORY": "OFF",
    "SLEW_ACCELERATION_DIST": "5.0",
    "SLEW_RAPID_STOP_DIST": "2.0",
    "GOTO_FEATURE": "ON",
    "GOTO_OFFSET": "0.25",
    "GOTO_OFFSET_ALIGN": "OFF",
    "MFLIP_SKIP_HOME": "OFF",
    "MFLIP_AUTOMATIC_DEFAULT": "OFF",
    "MFLIP_AUTOMATIC_MEMORY": "OFF",
    "MFLIP_PAUSE_HOME_DEFAULT": "OFF",
    "MFLIP_PAUSE_HOME_MEMORY": "OFF",
    "PIER_SIDE_SYNC_CHANGE_SIDES": "OFF",
    "PIER_SIDE_PREFERRED_DEFAULT": "BEST",
    "PIER_SIDE_PREFERRED_MEMORY": "OFF",
    "ALIGN_AUTO_HOME": "OFF",
    "ALIGN_MODEL_MEMORY": "OFF",
    "ALIGN_MAX_STARS": "AUTO",
    "AXIS3_DRIVER_MODEL": "OFF",
    "AXIS3_SLEW_RATE_BASE_DESIRED": "1.0",
    "AXIS3_STEPS_PER_DEGREE": "64.0",
    "AXIS3_LIMIT_MIN": "0",
    "AXIS3_LIMIT_MAX": "360",
    "AXIS3_REVERSE": "OFF",
    "AXIS3_POWER_DOWN": "OFF",
    "AXIS3_SENSE_HOME": "OFF",
    "AXIS3_DRIVER_STATUS": "OFF",
    "AXIS3_DRIVER_MICROSTEPS": "OFF",
    "AXIS3_DRIVER_MICROSTEPS_GOTO": "OFF",
    "AXIS3_DRIVER_IHOLD": "OFF",
    "AXIS3_DRIVER_IRUN": "OFF",
    "AXIS3_DRIVER_IGOTO": "OFF",
    "AXIS3_DRIVER_DECAY": "OFF",
    "AXIS3_DRIVER_DECAY_GOTO": "OFF",
    "AXIS3_SENSE_LIMIT_MIN": "OFF",
    "AXIS3_SENSE_LIMIT_MAX": "OFF",
    "AXIS4_DRIVER_MODEL": "OFF",
    "AXIS4_SLEW_RATE_BASE_DESIRED": "500",
    "AXIS4_SLEW_RATE_MINIMUM": "20",
    "AXIS4_STEPS_PER_MICRON": "0.5",
    "AXIS4_LIMIT_MIN": "0",
    "AXIS4_LIMIT_MAX": "50",
    "AXIS4_REVERSE": "OFF",
    "AXIS4_POWER_DOWN": "OFF",
    "AXIS4_SENSE_HOME": "OFF",
    "AXIS4_DRIVER_STATUS": "OFF",
    "AXIS4_DRIVER_MICROSTEPS": "OFF",
    "AXIS4_DRIVER_MICROSTEPS_GOTO": "OFF",
    "AXIS4_DRIVER_IHOLD": "OFF",
    "AXIS4_DRIVER_IRUN": "OFF",
    "AXIS4_DRIVER_IGOTO": "OFF",
    "AXIS4_DRIVER_DECAY": "OFF",
    "AXIS4_DRIVER_DECAY_GOTO": "OFF",
    "AXIS4_SENSE_LIMIT_MIN": "OFF",
    "AXIS4_SENSE_LIMIT_MAX": "OFF",
    "FOCUSER_TEMPERATURE": "OFF"
}

for i in range(1, 9):
    default_config.update({
        f"FEATURE{i}_PURPOSE": "OFF",
        f"FEATURE{i}_NAME": f"FEATURE{i}",
        f"FEATURE{i}_TEMP": "OFF",
        f"FEATURE{i}_PIN": "OFF",
        f"FEATURE{i}_VALUE_DEFAULT": "OFF",
        f"FEATURE{i}_VALUE_MEMORY": "OFF",
        f"FEATURE{i}_ON_STATE": "HIGH"
    })

@app.route('/', methods=['GET', 'POST'])
def index():
    config = default_config.copy()
    if request.method == 'POST':
        if 'generate' in request.form:
            config.update(request.form.to_dict())
            config_content = generate_config(config)
            return send_file(
                io.BytesIO(config_content.encode()),
                mimetype='text/plain',
                as_attachment=True,
                download_name='Config.h'
            )
        elif 'save' in request.form:
            config.update(request.form.to_dict())
            return Response(
                json.dumps(config, indent=2),
                mimetype='application/json',
                headers={'Content-Disposition': 'attachment;filename=preset.json'}
            )
        elif 'load' in request.files:
            file = request.files['load']
            if file and file.filename.endswith('.json'):
                preset = json.load(file)
                config.update(preset)
    return render_template('index.html', config=config)

if __name__ == '__main__':
    app.run(debug=True)