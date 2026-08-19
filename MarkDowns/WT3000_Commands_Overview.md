# WT3000 Communication Commands Übersicht

Diese Übersicht wurde auf maximal geringen Token-Verbrauch optimiert.
Um Redundanz zu vermeiden:
- `?` am Ende bedeutet "Query" (Abfrage).
- Das Präfix der Gruppe wurde bei den Unterbefehlen weggelassen (z.B. `:ACQuisition:BYTeorder` ist nur als `:BYTeorder` gelistet).
- Standard-Phrasen wie "Sets or queries" wurden auf "Set/Query" gekürzt.

## ACQuisition
* `?` : Query all settings
* `:BYTeorder` : Set/Query byte order (FLOAT)
* `:END` / `:STARt` : Set/Query output end/start point
* `:FORMat` : Set/Query format (ASCii/FLOat)
* `:HOLD` : Hold/release data
* `:LENGth?` / `:SRATe?` : Query total points / sample rate
* `:SEND?` : Query data
* `:TRACe` : Set/Query target trace

## AOUTput
* `?` / `:NORMal?` : Query all
* `[:NORMal]:CHANnel<x>` : Set/Query items
* `[:NORMal]:IRTime` : Set/Query rated integration time
* `[:NORMal]:MODE<x>` : Set/Query rated value method
* `[:NORMal]:RATE<x>` : Set/Query manual rated values

## CBCycle
* `?` : Query all
* `:COUNt` / `:TIMEout` : Set/Query cycles / timeout
* `:DISPlay` : Display settings (CURSor, ITEM<x>, PAGE)
* `:FILTer` : Filter settings (LINE, MOTor)
* `:RESet` / `:STARt` : Reset/start measurement
* `:STATe?` : Query status
* `:SYNChronize` : Sync settings (SLOPe, SOURce)
* `:TRIGger` : Trigger config (LEVel, MODE, SLOPe, SOURce)

## COMMunicate
* `?` : Query all
* `:HEADer` : Header on/off
* `:LOCKout` : Local lockout
* `:OPSE` / `:OPSR?` : Operation pending status
* `:OVERlap` : Set/Query overlap cmds
* `:REMote` : Remote/local
* `:STATus?` : Query status
* `:VERBose` : Full spelling/abbreviation
* `:WAIT` / `:WAIT?` : Wait for events

## CURSor
* `?` : Query all
* `:BAR` : Bar graph cursor (POSition, STATe, Y/DY)
* `:FFT` : FFT cursor (POSition, STATe, TRACe, X/DX/Y/DY)
* `:TRENd` : Trend cursor (POSition, STATe, TRACe, X/Y/DY)
* `:WAVE` : Waveform cursor (PATH, POSition, STATe, TRACe, X/DX/Y/DY)

## DISPlay
* `?` : Query all
* `:BAR` : Bar graph (FORMat, ITEM, ORDer)
* `:CBCycle` : Cycle display (CURSor, ITEM, PAGE)
* `:FFT` : FFT config (LABel, OBJect, STATe, FORMat, POINt, SCOPe, SPECtrum, VSCale, WINDow)
* `:FLICker` : Flicker display (ELEMent, PAGE, PERiod)
* `:INFOrmation` : Setup parameter list
* `:MATH` : Math display (CONStant, EXPRession, LABel, SCALing, UNIT)
* `:MODE` : Set/Query mode
* `:NUMeric` : Numeric display (ALL, FORMat, LIST, VAL4/8/16)
* `:TRENd` : Trend display (ALL, CLEar, FORMat, ITEM, SCALing, TDIV)
* `:VECTor` : Vector display (NUMeric, OBJect, UMAG/IMAG)
* `:WAVE` : Waveform display (ALL, FORMat, GRATicule, INTerpolate, MAPPing, POSition, SVALue, TDIV, TLABel, TRIGger, VZoom)

## FILE
* `?` : Query all
* `:CDIRectory` / `:MDIRectory` / `:PATH?` : Directory ops
* `:DELete` : Delete files (IMAGe, NUMeric, SETup, WAVE)
* `:DRIVe` / `:FORMat:EXECute` / `:FREE?` : Drive ops
* `:LOAD` / `:SAVE` : Load/Save files (ACQuisition, NUMeric, SETup, WAVE)

## FLICker
* `?` : Query all
* `:COUNt`, `:DC`, `:DMAX`, `:DMIN`, `:DT` : Limits & parameters
* `:EDITion`, `:ELEMent<x>`, `:FREQuency` : Targets & standard
* `:INITialize`, `:JUDGe`, `:MEASurement`, `:MOVe` : Operations
* `:PLT`, `:PST`, `:P3D3`, `:P4D15` : Pst/Plt settings
* `:RESet`, `:STARt`, `:STATe?` : Control
* `:TMAX`, `:UN`, `:VOLTage` : Limits & voltage

## HARMonics
* `?` : Query all
* `:FBANd` : Frequency bandwidth
* `:IEC` : IEC standard settings (OBJect, UGRouping/IGRouping)
* `:ORDer` : Max/min orders
* `:PLLSource` / `:PLLWarning` : PLL settings
* `:THD` : THD equation

## HCOPY
* `?` : Query all
* `:ABORt` / `:EXECute` : Process control
* `:AUTO` : Auto print (INTerval, START/END, STATe, SYNChronize)
* `:COMMent` / `:DIRection` : Output config
* `:NETPrint` : Network printer (COLor, FORMat)
* `:PRINter` : Built-in printer (FEED, FORMat, LIST)

## HOLD / IMAGe / INPut / INTEGrate
* `:HOLD` : Hold data output
* `:IMAGe` : Image saving (ABORt, COLor, COMMent, COMPression, EXECute, FORMat, SAVE, SEND)
* `:INPut` : Input config (CFACtor, CURRent, FILTer, INDependent, MODUle, NULL, POVer, SCALing, SYNChronize, VOLTage, WIRing)
* `:INTEGrate` : Integration (ACAL, MODE, RESet, RTIMe, STARt, STATe, STOP, TIMer)

## MEASure / MOTor / NUMeric
* `:MEASure` : Computation (AVERaging, COMPensation, DMeasure, EFFiciency, FREQuency, FUNCtion, MHOLd, PC, PHASe, SAMPling, SQFormula, SYNChronize)
* `:MOTor` : Motor eval (FILTer, PM, POLE, SPEed, SPeed, SYNChronize, TORQue)
* `:NUMeric` : Numeric data output (CBCycle, FLICker, FORMat, HOLD, LIST, NORMal)

## RATE / STATus / STORe / SYSTem / WAVeform
* `:RATE` : Data update interval
* `:STATus` : Comm status (CONDition, EESE, EESR, ERRor, FILTer, QENable, QMESsage, SPOLl)
* `:STORe` : Store/recall config (COUNt, DIRection, FILE, INTerval, ITEM, MEMory, MODE, NUMeric, RECall, RTIMe, SMODe, STARt, STOP, WAVE)
* `:SYSTem` : System config (CLOCk, DATE, ECLear, FONT, KLOCk, LANGuage, LCD, SLOCk, TIME, USBKeyboard)
* `:WAVeform` : Waveform data output (BYTeorder, END, FORMat, HOLD, LENGth, SEND, SRATe, STARt, TRACe, TRIGger)

## Common Commands
* `*CAL?`, `*CLS`, `*ESE`, `*ESR?`, `*IDN?`, `*OPC`, `*OPC?`, `*OPT?`, `*PSC`, `*RST`, `*SRE`, `*STB?`, `*TRG`, `*TST?`, `*WAI`
