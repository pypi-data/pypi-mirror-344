import os,sys,time

def help():
    print("""Usage: uaua -l TIME_SEC -c LINE_COUNT -t TEXT

-l, --duration        Time in seconds until the uauator gets stopped.
-c, --line-count       How many lines the uauator should print out.
-t, --text             Custom text instead of 'uaua\\n'.
""",file=sys.stderr)
    sys.exit(1)

def processArgument(option,arg):
    try:
        identifier=None
        processed=None
        match option:
            case "l"|"duration":
                identifier="duration"
                processed=float(arg)
                if processed<1: raise ValueError("duration must be higher than 0")
            case "c"|"line-count":
                identifier="lineCount"
                processed=int(arg)
                if processed<1: raise ValueError("line count must be 1 or higher")
            case "t"|"text":
                identifier="text"
                processed=arg
            case _: raise ValueError("unknown argument")
        return identifier,processed
    except Exception as e:
        print(f"[!] Failed parsing argument {option}={arg!r}: {e!s}",file=sys.stderr)
        help()

def main(argv):
    args={
    "duration":None,
    "lineCount":None,
    "text":"uaua\n",
    }
    for a in argv[1:]:
        if a in ("-h","-?","--help","/?","/h"): help()
    option=None
    for arg in argv[1:]:
        print(arg,file=sys.stderr)
        if option==None:
            option=arg.lstrip("-").lstrip("/")
        else:
            processed=processArgument(option,arg)
            if processed!=None: args[processed[0]]=processed[1]
            option=None
    duration=args["duration"]
    lineCount=args["lineCount"]
    text=args["text"]
    if duration and lineCount:
        print("[!] You can't specify both line count and duration",file=sys.stderr)
        help()
    stream=sys.stdout
    lines=0
    startTime=time.time()
    try:
        if duration:
            while time.time()-startTime<=duration:
                lines+=1
                stream.write(text)
        elif lineCount:
            while lines<lineCount:
                lines+=1
                stream.write(text)
        else:
            while True:
                lines+=1
                stream.write(text)
    except KeyboardInterrupt: pass
    duration=time.time()-startTime
    strDuration=f"{duration:.8f}"
    strLines=str(lines)
    uauaPerSec=lines/duration
    strUauaPerSec=f"{uauaPerSec:.2f}"
    secPerUaua=duration/lines
    strSecPerUaua=f"{secPerUaua:.9f}"
    outputWidth=max(len(strLines),len(strUauaPerSec),len(strSecPerUaua))+2
    print(f"{strDuration.rjust(outputWidth)} seconds taken\n{strLines.rjust(outputWidth)} uaua\n{strUauaPerSec.rjust(outputWidth)} uaua per second\n{strSecPerUaua.rjust(outputWidth)} seconds per uaua",file=sys.stderr)
