import controls
import engine_factory
from audio_device import AudioDevice
import obd
import time
import multiprocessing

# engine = engine_factory.v_four_90_deg()
# engine = engine_factory.w_16()
# engine = engine_factory.v_8_LS()
# engine = engine_factory.inline_5_crossplane()
# engine = engine_factory.inline_6()
# engine = engine_factory.boxer_4_crossplane_custom([100, 100, 0, 0])  # (rando := random.randrange(360)))
# engine = engine_factory.inline_4_1_spark_plug_disconnected()
# engine = engine_factory.inline_4()
# engine = engine_factory.boxer_4_half()
# engine = engine_factory.random()
# engine = engine_factory.fake_rotary_2rotor()
# engine = engine_factory.V_12()

def engine_sound(speed_val):
    engine = engine_factory.v_four_90_deg() # Define engine sound to be simulated.
    audio_device = AudioDevice() # Define a new audio device.
    stream = audio_device.play_stream(engine.gen_audio) # Set the audio device to play desired engine sound.
    print('\nEngine is running...')

    #Block of code for throttling via OBD.
    while True:
        # print('speed_val: ', speed_val)
        engine.rpm_pull(speed_val.value)  

    #Block of code for throttling via manual input using keyboard.
    '''
    try:
        controls.capture_input(engine)  # blocks until user exits
    except KeyboardInterrupt:
        pass
    '''

    print('Exiting...')
    stream.close() # Stop sound.
    audio_device.close() # Close audio device.

def obd_connect(speed_val):
    ports = obd.scan_serial() # Scan for available ports.
    print('Found ports: ', ports) # Print any available ports.
    connection = obd.Async(ports[1]) # Establish connection to port 1.
    print('Connected!')

    def new_speed(spd):
        speed_val.value = round(spd.value.magnitude) # Set speed variable to new fetched value.
        print ('Updated to: ', speed_val.value)

    connection.watch(obd.commands.SPEED, callback=new_speed) # Set speed command to be continuosly updated.
    connection.start() # Start the async update loop.
    print('Fetch checkpoint.')

    time.sleep(120) # Set timeout for the loop.
    connection.stop() # Disconnect from OBD adapter.

if __name__ == '__main__':

    speed_val = multiprocessing.Value('i', 1)

    process1 = multiprocessing.Process(target = engine_sound, args=(speed_val,))
    process2 = multiprocessing.Process(target = obd_connect, args=(speed_val,))

    process2.start()
    process1.start()


