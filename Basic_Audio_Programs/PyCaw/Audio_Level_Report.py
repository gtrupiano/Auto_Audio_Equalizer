import time
from pycaw.pycaw import AudioUtilities, IAudioMeterInformation
import keyboard

class Audio_Sessions_Types:
    def __init__(self, Program: str, Audio_Level: int):
        self.Program = Program
        self.Audio_Level = Audio_Level
    
    #def __repr__(self):
    #    # Representation of the object when printing
    #    return f"{self.Program}: {self.Audio_Level * 100:.1f}%"

Program_Sessions = [] 

def Audio_Level_Report():
    #Monitors and displays audio levels for all active applications.
    sessions = AudioUtilities.GetAllSessions()
    if not sessions:
        print("No audio sessions found.")
        return
    
    while not keyboard.is_pressed("q"):
        print("\nApplication Audio Levels: ")
        for session in sessions:
            process = session.Process
            if process:
                # Query the audio meter information for this session
                try:
                    meter = session._ctl.QueryInterface(IAudioMeterInformation)
                    peak = meter.GetPeakValue()  # Peak audio level (0.0 to 1.0)
                    print(f"Application: {process.name()} Volume Level: {peak * 100:.1f}%")
                    existing_app = next((s for s in Program_Sessions if s.Program == process.name()), None) # if program already exists in list, then return true else false (basically)ff
                    if(existing_app):
                        existing_app.Audio_Level = peak
                    else:
                        Program_Sessions.append(Audio_Sessions_Types(Program = process.name(), Audio_Level = peak))

                except Exception as e:
                    print(f"Could not retrieve audio level for {process.name()}: {e}")

        time.sleep(0.1)

    print("\nStopping monitoring...")
    # Print the final state of the list
    print("\nFinal Program Sessions List:")
    for program in Program_Sessions:
        #print(program.Program + " " + str(int((program.Audio_Level)*100)) + "%")
        print(f"{program.Program}: {program.Audio_Level * 100:.1f}%")

# Run the audio monitoring
Audio_Level_Report()