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

# Check audio levels for all applications and saves them in list
def Audio_Level_Report():
    sessions = AudioUtilities.GetAllSessions()
    if not sessions:
        print("No audio sessions found.")
        return
    
    #print("\nApplication Audio Levels: ")
    for session in sessions:
        process = session.Process
        if process:
            # Query the audio meter information for this session
            try:
                meter = session._ctl.QueryInterface(IAudioMeterInformation)
                peak = meter.GetPeakValue()  # Peak audio level (0.0 to 1.0)
                #print(f"Application: {process.name()} Volume Level: {peak * 100:.1f}%")
                existing_app = next((s for s in Program_Sessions if s.Program == process.name()), None) # if program already exists in list, then return true else false (basically)ff
                if(existing_app):
                    existing_app.Audio_Level = peak
                else:
                    Program_Sessions.append(Audio_Sessions_Types(Program = process.name(), Audio_Level = peak))

            except Exception as e:
                print(f"Could not retrieve audio level for {process.name()}: {e}")
        
        time.sleep(0.1)


def Audio_Level_Range():
    print("Obtaining Audio Levels: ")
    Audio_Level_Report()
    
    for program in Program_Sessions:
        print("Program " + str(program) + " : " + str(Program_Sessions[program].Program) + "\n")
    
    limitedProgram = input("Type 1 - X according to the list to limit a specific application: ")

    highProgramLimit = input("Type highest audio value wanted for this program: ")
    lowProgramLimit = input("Type lowest audio value wanted for this program: ")

    listSize = 0

    # if(limitedProgram == 1):
    #     if(Program_Sessions[1])
        