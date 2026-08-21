# WT3000 Communication Commands

Markdown transcription of Chapter 6, "Communication Commands," from `WT3000_Communication_Commands.pdf`.

> The original document uses a two-column layout on many pages. For those pages, the left column is followed by the right column.

## Page 6-1

```text
   Chapter 6 Communication Commands

     6.1    List of Commands

     Command              Function                              Page

     ACQuisition Group
     :ACQuisition?        Queries all settings related to the output of the waveform sampling data. 6-17
     :ACQuisition:BYTeorder Sets the output byte order of the waveform sampling data (FLOAT format) 6-17
                          that is transmitted by “:ACQuisition:SEND?” or queries the current
                          setting.
     :ACQuisition:END     Sets the output end point of the waveform display data that is transmitted by 6-17
                          “:ACQuisition:SEND?” or queries the current setting.
     :ACQuisition:FORMat  Sets the format of the waveform sampling data that is transmitted by 6-17
                          “:ACQuisition:SEND?” or queries the current setting.
     :ACQuisition:HOLD    Sets whether to hold (ON) or release (OFF) all the waveform sampling data 6-17
                          or queries the current setting.
     :ACQuisition:LENGth? Queries the total number of points of the waveform sampling specified by 6-18
                          “:ACQuisition:TRACe.”
     :ACQuisition:SEND?   Queries the waveform sampling data specified by “:ACQuisition:TRACe.” 6-18
     :ACQuisition:SRATe?  Queries the sampling rate of the retrieved data 6-18
     :ACQuisition:STARt   Sets the output start point of the waveform display data that is transmitted by 6-18
                          “:ACQuisition:SEND?” or queries the current setting.
     :ACQuisition:TRACe   Sets the target trace of “:ACQuisition:SEND?” or queries the current 6-18
                          setting.
     AOUTput Group
     :AOUTput?            Queries all settings related to the D/A output. 6-19
     :AOUTput:NORMal?     Queries all settings related to the D/A output. 6-19
     :AOUTput[:NORMal]:CHANnel<x> Sets the D/A output items (function, element, and harmonic order) or queries 6-19
                          the current setting.
     :AOUTput[:NORMal]:IRTime Sets the rated integration time for the D/A output of integrated values or 6-19
                          queries the current setting.
     :AOUTput[:NORMal]:MODE<x> Sets the method of setting the rated value for the D/A output items or queries 6-20
                          the current setting.
     :AOUTput[:NORMal]:RATE<x> Manually sets the rated maximum and minimum values for the D/A output 6-20
                          items or queries the current setting.
     CBCycle Group
     :CBCycle?            Queries all settings related to the Cycle by Cycle measurement function. 6-21
     :CBCycle:COUNt       Sets the number of cycles for Cycle by Cycle measurement or queries the 6-21
                          current setting.
     :CBCycle:DISPlay?    Queries all settings related to the Cycle by Cycle display. 6-21
     :CBCycle:DISPlay:CURSor Sets the cursor position of the Cycle by Cycle display or queries the current 6-21
                          setting.
     :CBCycle:DISPlay:ITEM<x> Sets the displayed items (function and element) of the Cycle by Cycle display 6-21
                          or queries the current setting.
     :CBCycle:DISPlay:PAGE Sets the number of the displayed page of the Cycle by Cycle display or 6-21
                          queries the current setting.
     :CBCycle:FILTer?     Queries all settings related to the filter for Cycle by Cycle measurement. 6-22
     :CBCycle:FILTer:LINE? Queries all settings related to the line filter for Cycle by Cycle measurement. 6-22
     :CBCycle:FILTer[:LINE][:ALL] Collectively sets the line filters of all elements for Cycle by Cycle 6-22
                          measurement
     :CBCycle:FILTer[:LINE]:ELEMent Sets the line filter of individual elements for Cycle by Cycle measurement or 6-22
     <x>                  queries the current setting
     :CBCycle:FILTer[:LINE]:MOTor Sets the motor input line filters for Cycle by Cycle measurement or queries 6-22
                          the current setting
     :CBCycle:RESet       Resets Cycle by Cycle measurement.    6-22
     :CBCycle:STARt       Starts Cycle by Cycle measurement.    6-22
     :CBCycle:STATe?      Queries the Cycle by Cycle measurement status. 6-22
     :CBCycle:SYNChronize? Queries all settings related to the synchronization source for Cycle by Cycle 6-22
                          measurement.
```

## Page 6-2

```text
 6.1 List of Commands

   Command              Function                              Page
   :CBCycle:SYNChronize:SLOPe Sets the slope of the synchronization source of Cycle by Cycle measurement 6-22
                        or queries the current setting.
   :CBCycle:SYNChronize:SOURce Sets the synchronization source for Cycle by Cycle measurement or queries 6-23
                        the current setting.
   :CBCycle:TIMEout     Sets the timeout value for Cycle by Cycle measurement or queries the 6-23
                        current setting.
   :CBCycle:TRIGger?    Queries all settings related to triggers or queries the current setting. 6-23
   :CBCycle:TRIGger:LEVel Sets the trigger level or queries the current setting. 6-23
   :CBCycle:TRIGger:MODE Sets the trigger mode or queries the current setting. 6-23
   :CBCycle:TRIGger:SLOPe Sets the trigger slope or queries the current setting. 6-23
   :CBCycle:TRIGger:SOURce Sets the trigger source or queries the current setting. 6-23
   COMMunicate Group
   :COMMunicate?        Queries all settings related to communications. 6-24
   :COMMunicate:HEADer  Sets whether to add a header to the response to a query (example 6-24
                        DISPLAY:MODE NUMERIC) or not add the header (example NUMERIC).
   :COMMunicate:LOCKout Sets or clears local lockout.         6-24
   :COMMunicate:OPSE(Operation Sets the overlap command that is used by the *OPC, *OPC?, and *WAI 6-24
   Pending Status Enable register) commands or queries the current setting.
   :COMMunicate:OPSR?(Operation Queries the value of the operation pending status register. 6-24
   Pending Status Register)
   :COMMunicate:OVERlap Sets the commands that will operate as overlap commands or queries the 6-24
                        current setting.
   :COMMunicate:REMote  Sets remote or local. ON is remote mode. 6-24
   :COMMunicate:STATus? Queries line-specific status.         6-25
   :COMMunicate:VERBose Sets whether to return the response to a query using full spelling (example 6-25
                        :INPUT:VOLTAGE:RANGE:ELEMENT1 1.000E+03) or using abbreviation
                        (example :VOLT:RANG:ELEM 1.000E+03).
   :COMMunicate:WAIT    Waits for one of the specified extended events to occur. 6-25
   :COMMunicate:WAIT?   Creates the response that is returned when the specified event occurs. 6-25
   CURSor Group
   :CURSor?             Queries all settings related to the cursor measurement. 6-26
   :CURSor:BAR?         Queries all settings related to the cursor measurement of the bar graph 6-26
                        display.
   :CURSor:BAR:POSition<x> Sets the cursor position (order) on the bar graph display or queries the 6-26
                        current setting.
   :CURSor:BAR[:STATe]  Turns ON/OFF the cursor display on the bar graph display or queries the 6-26
                        current setting.
   :CURSor:BAR:{Y<x>|DY}? Queries the cursor measurement value on the bar graph display. 6-26
   :CURSor:FFT?         Queries all settings related to the cursor measurement on the FFT waveform 6-26
                        display.
   :CURSor:FFT:POSition<x> Sets the cursor position on the FFT waveform display or queries the current 6-26
                        setting.
   :CURSor:FFT[:STATe]  Turns ON/OFF the cursor display on the FFT waveform display or queries 6-27
                        the current setting.
   :CURSor:FFT:TRACe<x> Sets the cursor target on the FFT waveform display or queries the current 6-27
                        setting.
   :CURSor:FFT:{X<x>|DX|Y<x>|DY}? Queries the cursor measurement value on the FFT waveform display. 6-27
   :CURSor:TRENd?       Queries all settings related to the cursor measurement of the trend display. 6-27
   :CURSor:TRENd:POSition<x> Sets the cursor position on the trend display or queries the current setting. 6-27
   :CURSor:TRENd[:STATe] Turns ON/OFF the cursor display on the trend display or queries the current 6-27
                        setting.
   :CURSor:TRENd:TRACe<x> Sets the cursor target on the trend display or queries the current setting. 6-27
   :CURSor:TRENd:{X<x>|Y<x>|DY}? Queries the cursor measurement value on the trend display. 6-27
   :CURSor:WAVE?        Queries all settings related to the cursor measurement on the waveform 6-28
                        display.
   :CURSor:WAVE:PATH    Sets the cursor path on the waveform display or queries the current setting. 6-28
   :CURSor:WAVE:POSition<x> Sets the cursor position on the waveform display or queries the current 6-28
                        setting.
```

## Page 6-3

```text
                                                      6.1 List of Commands

     Command              Function                              Page
     :CURSor:WAVE[:STATe] Turns ON/OFF the cursor display on the waveform display or queries the 6-28
                          current setting.
     :CURSor:WAVE:TRACe<x> Sets the cursor target on the waveform display or queries the current setting. 6-28
     :CURSor:WAVE:{X<x>|DX|PERDt|Y<x Queries the cursor measurement value on the waveform display. 6-28
     >|DY}?
     DISPlay Group
     :DISPlay?            Queries all settings related to the screen display. 6-29
     :DISPlay:BAR?        Queries all settings related to the bar graph. 6-29
     :DISPlay:BAR:FORMat  Sets the display format of the bar graph or queries the current setting. 6-29
     :DISPlay:BAR:ITEM<x> Sets the bar graph item (function and element) or queries the current setting. 6-29
     :DISPlay:BAR:ORDer   Sets the start and end orders of the bar graph or queries the current setting. 6-30
     :DISPlay:CBCycle?    Queries all settings related to the Cycle by Cycle display. 6-30
     :DISPlay:CBCycle:CURSor Sets the cursor position of the Cycle by Cycle display or queries the current 6-30
                          setting.
     :DISPlay:CBCycle:ITEM<x> Sets the displayed items (function and element) of the Cycle by Cycle display 6-30
                          or queries the current setting.
     :DISPlay:CBCycle:PAGE Sets the number of the displayed page of the Cycle by Cycle display or 6-30
                          queries the current setting.
     :DISPlay:FFT?        Queries all settings related to the FFT waveform display. 6-30
     :DISPlay:FFT:FFT<x>? Queries all settings related to the FFT waveform. 6-31
     :DISPlay:FFT:FFT<x>:LABel Sets the label of the FFT waveform or queries the current setting. 6-31
     :DISPlay:FFT:FFT<x>:OBJect Sets the source waveform of the FFT computation or queries the current 6-31
                          setting.
     :DISPlay:FFT:FFT<x>[:STATe] Turns ON/OFF the FFT waveform display or queries the current setting. 6-31
     :DISPlay:FFT:FORMat  Sets the display format of the FFT waveform or queries the current setting. 6-31
     :DISPlay:FFT:POINt   Sets the number of points of the FFT computation or queries the current 6-31
                          setting.
     :DISPlay:FFT:SCOPe   Sets the display range of the FFT waveform or queries the current setting. 6-31
     :DISPlay:FFT:SPECtrum Sets the display spectrum format of the FFT waveform or queries the current 6-32
                          setting.
     :DISPlay:FFT:VSCale  Sets the display scale of the vertical axis of the FFT waveform or queries the 6-32
                          current setting.
     :DISPlay:FFT:WINDow  Sets the window function of the FFT computation or queries the current 6-32
                          setting.
     :DISPlay:FLICker?    Queries all settings related to flicker measurement display. 6-32
     :DISPlay:FLICker:ELEMent Sets the element to be displayed for flicker measurement display or queries 6-32
                          the current setting.
     :DISPlay:FLICker:PAGE Sets the page numbers to be displayed for flicker measurement display or 6-32
                          queries the current setting.
     :DISPlay:FLICker:PERiod Sets the display observation period number for flicker measurement display 6-32
                          or queries the current setting.
     :DISPlay:INFOrmation? Queries all settings related to the display of the setup parameter list. 6-32
     :DISPlay:INFOrmation:PAGE Sets the page number of the display of setup parameter list or queries the 6-32
                          current setting.
     :DISPlay:INFOrmation[:STATe] Turns ON/OFF the display of the setup parameter list or queries the current 6-32
                          setting.
     :DISPlay:MATH?       Queries all settings related to the computed waveform display. 6-33
     :DISPlay:MATH:CONStant<x> Sets the constant to be used in the waveform computing equation or queries 6-33
                          the current setting.
     :DISPlay:MATH:MATH<x>? Queries all settings related to the computed waveform. 6-33
     :DISPlay:MATH:MATH<x>:EXPRessi Sets the equation of the waveform computation or queries the current 6-33
     on                   setting.
     :DISPlay:MATH:MATH<x>:LABel Sets the label of the computed waveform or queries the current setting. 6-33
     :DISPlay:MATH:MATH<x>:SCALing? Queries all settings related to the scaling of the computed waveform. 6-33
     :DISPlay:MATH:MATH<x>:SCALing:C Sets the center value of the manual scaling of the computed waveform or 6-34
     ENTer                queries the current setting.
     :DISPlay:MATH:MATH<x>:SCALing:M Sets the scaling mode of the computed waveform or queries the current 6-34
     ODE                  setting.
     :DISPlay:MATH:MATH<x>:SCALing:S Sets the scale/division value of the manual scaling of the computed 6-34
     DIV                  waveform or queries the current setting.
```

## Page 6-4

```text
 6.1 List of Commands

   Command              Function                              Page
   :DISPlay:MATH:MATH<x>:UNIT Sets the unit to be added to the result of the waveform computation or 6-34
                        queries the current setting.
   :DISPlay:MODE        Sets the display mode or queries the current setting. 6-35
   :DISPlay:NUMeric?    Queries all settings related to the numeric display. 6-35
   :DISPlay:NUMeric:NORMal? Queries all settings related to the numeric display. 6-35
   :DISPlay:NUMeric[:NORMal]:ALL? Queries all settings related to the numeric display (all display). 6-35
   :DISPlay:NUMeric[:NORMal]:ALL:C Sets the cursor position on the numeric display (all display) or queries the 6-35
   URSor                current setting.
   :DISPlay:NUMeric[:NORMal]:ALL:O Sets the displayed harmonic order on the harmonic measurement function 6-36
   RDer                 display page of the numeric display (all display) or queries the current
                        setting.
   :DISPlay:NUMeric[:NORMal]:ALL:P Sets the page number on the numeric display (all display) or queries the 6-36
   AGE                  current setting.
   :DISPlay:NUMeric[:NORMal]:FORM Sets the numeric display format or queries the current setting. 6-36
   at
   :DISPlay:NUMeric[:NORMal]:LIST? Queries all settings related to the numeric display (list display). 6-36
   :DISPlay:NUMeric[:NORMal]:LIST: Sets the cursor position on the numeric display (list display) or queries the 6-37
   CURSor               current setting.
   :DISPlay:NUMeric[:NORMal]:LIST: Sets the cursor position in the header section on the numeric display (list 6-37
   HEADer               display) or queries the current setting.
   :DISPlay:NUMeric[:NORMal]:LIST: Sets the displayed items (function and element) on the numeric display (list 6-37
   ITEM<x>              display) or queries the current setting.
   :DISPlay:NUMeric[:NORMal]:LIST: Sets the harmonic order cursor position in the data section on the numeric 6-37
   ORDer                display (list display) or queries the current setting.
   :DISPlay:NUMeric[:NORMal]:{VAL4 Queries all settings related to the numeric display ({4-value|8-value|16-value} 6-38
   |VAL8|VAL16}?        display).
   :DISPlay:NUMeric[:NORMal]:{VAL4 Sets the cursor position on the numeric display ({4-value|8-value|16-value} 6-38
   |VAL8|VAL16}:CURSor  display) or queries the current setting.
   :DISPlay:NUMeric[:NORMal]:{VAL4 Sets the displayed items (function, element, and harmonic order) on the 6-38
   |VAL8|VAL16}:ITEM<x> numeric display ({4-value|8-value|16-value} display) or queries the current
                        setting.
   :DISPlay:NUMeric[:NORMal]:{VAL4 Sets the page number on the numeric display ({4-value|8-value|16-value} 6-38
   |VAL8|VAL16}:PAGE    display) or queries the current setting.
   :DISPlay:NUMeric[:NORMal]:{VAL4 Sets the displayed items on the numeric display ({4-value|8-value|16-value} 6-39
   |VAL8|VAL16}:PRESet  display) to a preset pattern.
   :DISPlay:TRENd?      Queries all settings related to the trend. 6-39
   :DISPlay:TRENd:ALL   Collectively turns ON/OFF all trends. 6-39
   :DISPlay:TRENd:CLEar Clears the trend.                     6-39
   :DISPlay:TRENd:FORMat Sets the display format of the trend or queries the current setting. 6-39
   :DISPlay:TRENd:ITEM<x>? Queries all settings related to the trend. 6-39
   :DISPlay:TRENd:ITEM<x>[:FUNCti Sets the trend item (function, element, and harmonic order) or queries the 6-39
   on]                  current setting.
   :DISPlay:TRENd:ITEM<x>:SCALing? Queries all settings related to the scaling of the trend. 6-39
   :DISPlay:TRENd:ITEM<x>:SCALing: Sets the scaling mode of the trend or queries the current setting. 6-40
   MODE
   :DISPlay:TRENd:ITEM<x>:SCALing: Sets the upper and lower limits of manual scaling of the trend or queries the 6-40
   VALue                current setting.
   :DISPlay:TRENd:TDIV  Sets the horizontal axis (T/div) of the trend or queries the current setting. 6-40
   :DISPlay:TRENd:T<x>  Turns ON/OFF the trend or queries the current setting. 6-40
   :DISPlay:VECTor?     Queries all settings related to the vector display. 6-40
   :DISPlay:VECTor:NUMeric Turns ON/OFF the numeric data display for the vector display or queries the 6-40
                        current setting.
   :DISPlay:VECTor:OBJect Sets the wiring unit to be displayed during vector display or queries the 6-40
                        current setting.
   :DISPlay:VECTor:{UMAG|IMAG} Sets the zoom factor of the {voltage|current} display during vector display or 6-41
                        queries the current setting.
   :DISPlay:WAVE?       Queries all settings related to the waveform display. 6-41
   :DISPlay:WAVE:ALL    Collectively turns ON/OFF all waveform displays. 6-41
   :DISPlay:WAVE:FORMat Sets the display format of the waveform or queries the current setting. 6-41
   :DISPlay:WAVE:GRATicule Sets the graticule (grid) type or queries the current setting. 6-41
   :DISPlay:WAVE:INTerpolate Sets the interpolation method of the waveform or queries the current setting. 6-41
   :DISPlay:WAVE:MAPPing? Queries all settings related to the waveform mapping to the split screen. 6-41
```

## Page 6-5

```text
                                                      6.1 List of Commands

     Command              Function                              Page
     :DISPlay:WAVE:MAPPing[:MODE] Sets the waveform mapping method for the split screen or queries the 6-41
                          current setting.
     :DISPlay:WAVE:MAPPing:{U<x>|I<x Sets the mapping of the {voltage|current|rotating speed|torque|waveform 6-42
     >|SPEed|TORQue|MATH<x>} computation} waveform to the split screen or queries the current setting.
     :DISPlay:WAVE:POSition? Queries all settings related to the vertical position (level of the center 6-42
                          position) of the waveform.
     :DISPlay:WAVE:POSition:{UALL|IA Collectively sets the vertical position (level of the center position) of the 6-42
     LL}                  waveform {voltage|current} of all elements.
     :DISPlay:WAVE:POSition:{U<x>|I Sets the vertical position (level of the center position) of the waveform 6-42
     <x>}                 {voltage|current} of the element or queries the current setting.
     :DISPlay:WAVE:SVALue (Scale Turns ON/OFF the scale value display or queries the current setting. 6-42
     VALue)
     :DISPlay:WAVE:TDIV   Sets the Time/div value of the waveform or queries the current setting. 6-42
     :DISPlay:WAVE:TLABel (Trace Turns ON/OFF the waveform label display or queries the current setting. 6-42
     LABel)
     :DISPlay:WAVE:TRIGger? Queries all settings related to the trigger. 6-42
     :DISPlay:WAVE:TRIGger:LEVel Sets the trigger level or queries the current setting. 6-42
     :DISPlay:WAVE:TRIGger:MODE Sets the trigger mode or queries the current setting. 6-43
     :DISPlay:WAVE:TRIGger:SLOPe Sets the trigger slope or queries the current setting. 6-43
     :DISPlay:WAVE:TRIGger:SOURce Sets the trigger source or queries the current setting. 6-43
     :DISPlay:WAVE:{U<x>|I<x>|SPEed| Turns ON/OFF the {voltage|current|rotating speed|torque|waveform 6-43
     TORQue|MATH<x>}      computation} waveform or queries the current setting.
     :DISPlay:WAVE:VZoom? Queries all settings related to the vertical zoom factor of the waveform. 6-43
     :DISPlay:WAVE:VZoom:{UALL|IALL} Collectively sets the vertical zoom factor of the waveform {voltage|current} of 6-43
                          all elements.
     :DISPlay:WAVE:VZoom:{U<x>|I<x>} Sets the vertical zoom factor of the waveform {voltage|current} of the element 6-43
                          or queries the current setting.
```

## Page 6-6

```text
 6.1 List of Commands

   Command              Function                              Page

   FILE Group
   :FILE?               Queries all settings related to the file operation. 6-47
   :FILE:CDIRectory     Changes the current directory.        6-47
   :FILE:DELete:IMAGe:{TIFF|BMP|PS Deletes the screen image data file. 6-47
   CRipt|PNG|JPEG}
   :FILE:DELete:NUMeric:{ASCii|FLO Deletes the numeric data file. 6-47
   at}
   :FILE:DELete:SETup   Deletes the setup parameter file.     6-47
   :FILE:DELete:WAVE:{BINary|ASCii Deletes the waveform display data file. 6-47
   |FLOat}
   :FILE:DRIVe          Sets the target drive.                6-47
   :FILE:FORMat:EXECute Formats the PC card.                  6-47
   :FILE:FREE?          Queries the free disk space (bytes) on the drive. 6-47
   :FILE:LOAD:ABORt     Aborts file loading.                  6-47
   :FILE:LOAD:SETup     Loads the setup parameter file.       6-47
   :FILE:MDIRectory     Creates a directory.                  6-48
   :FILE:PATH?          Queries the absolute path of the current directory. 6-48
   :FILE:SAVE?          Queries all settings related to the saving of files. 6-48
   :FILE:SAVE:ABORt     Aborts file saving.                   6-48
   :FILE:SAVE:ACQuisition? Queries all settings related to the file saving of the waveform sampling data. 6-48
   :FILE:SAVE:ACQuisition[:EXECu Saves the waveform sampling data to a file. 6-48
   te]
   :FILE:SAVE:ACQuisition:TRACe Sets the waveform sampling data to be saved to a file or queries the current 6-48
                        setting.
   :FILE:SAVE:ACQuisition:TYPE Sets the format of the waveform sampling data to be saved or queries the 6-48
                        current setting.
   :FILE:SAVE:ANAMing   Sets whether to automatically name the files to be saved or queries the 6-48
                        current setting.
   :FILE:SAVE:COMMent   Sets the comment to be added to the file to be saved or queries the current 6-48
                        setting.
   :FILE:SAVE:NUMeric?  Queries all settings related to the saving of numeric data files. 6-49
   :FILE:SAVE:NUMeric:CBCycle? Queries all settings related to Cycle by Cycle measurement items saved to 6-49
                        numeric data files or queries the current setting
   :FILE:SAVE:NUMeric:CBCycle:ALL Collectively turns ON/OFF the output of all elements and functions when 6-49
                        saving numeric data from Cycle by Cycle measurement to a file.
   :FILE:SAVE:NUMeric:CBCycle:{ELE Turns ON/OFF the output of {each element | ΣA | ΣB} when saving numeric 6-49
   Ment<x>|SIGMA|SIGMB} data from Cycle by Cycle measurement to a file.
   :FILE:SAVE:NUMeric:CBCycle:<Fun Turns ON/OFF the output of each function when saving numeric data from 6-49
   ction>               Cycle by Cycle measurement to a file or queries the current setting.
   :FILE:SAVE:NUMeric[:EXECute] Saves the numeric data to a file. 6-49
   :FILE:SAVE:NUMeric:NORMal? Queries all settings related to the items saved to numeric data files. 6-50
   :FILE:SAVE:NUMeric:NORMal:ALL Collectively turns ON/OFF the output of all element functions when saving the 6-50
                        numerical data file.
   :FILE:SAVE:NUMeric:NORMal:{ELEM Turns ON/OFF the output of {each element|ΣA|ΣB} when saving the numeric 6-50
   ent<x>|SIGMA|SIGMB}  data to file.
   :FILE:SAVE:NUMeric:NORMal:PRESe Presets the output ON/OFF pattern of the element function for saving the 6-50
   t<x>                 numeric data to file.
   :FILE:SAVE:NUMeric:NORMal:<Func Turns ON/OFF the output of the function when saving the numerical data file 6-50
   tion>                or queries the current setting.
   :FILE:SAVE:NUMeric:TYPE Sets the format of the numeric data to be saved or queries the current 6-50
                        setting.
   :FILE:SAVE:SETup[:EXECute] Saves of the setup parameter file. 6-50
   :FILE:SAVE:WAVE?     Queries all settings related to the saving of waveform display data files. 6-50
   :FILE:SAVE:WAVE[:EXECute] Executes the saving of the waveform display data file. 6-51
   :FILE:SAVE:WAVE:TRACe Sets the waveform to be saved or queries the current setting. 6-51
   :FILE:SAVE:WAVE:TYPE Sets the format of the waveform display data to be saved or queries the 6-51
                        current setting.
```

## Page 6-7

```text
                                                      6.1 List of Commands

     Command              Function                              Page

     FLICker Group
     :FLICker?            Queries all settings related to flicker measurement. 6-52
     :FLICker:COUNt       Sets the number of measurements for the short-term flicker value Pst or 6-52
                          queries the current setting.
     :FLICker:DC?         Sets all settings related to the relative steady-state voltage change dc or 6-52
                          queries the current setting.
     :FLICker:DC:LIMit    Sets the limit of the relative steady-state voltage change dc or queries the 6-52
                          current setting.
     :FLICker:DC[:STATe]  Turns ON/OFF judgment of the relative steady-state voltage change dc or 6-52
                          queries the current setting.
     :FLICker:DISPlay?    Queries all settings related to flicker measurement display. 6-52
     :FLICker:DISPlay:ELEMent Sets the element to be displayed for flicker measurement display or queries 6-52
                          the current setting.
     :FLICker:DISPlay:PAGE Sets the page numbers to be displayed for flicker measurement display or 6-53
                          queries the current setting.
     :FLICker:DISPlay:PERiod Sets the display observation period number for flicker measurement display 6-53
                          or queries the current setting.
     :FLICker:DMAX?       Sets all settings related to the maximum relative voltage change dmax or 6-53
                          queries the current setting.
     :FLICker:DMAX:LIMit  Sets the limit of the maximum relative voltage change dmax or queries the 6-53
                          current setting.
     :FLICker:DMAX[:STATe] Turns ON/OFF judgment of the maximum relative voltage change dmax or 6-53
                          queries the current setting.
     :FLICker:DMIN?       Sets all settings related to the steady-state range dmin or queries the current 6-53
                          setting.
     :FLICker:DMIN:LIMit  Sets the limit of the steady-state range dmin or queries the current setting. 6-53
     :FLICker:DT?         Sets all settings related to the relative voltage change time d(t) or queries the 6-53
                          current setting.
     :FLICker:DT:LIMit    Sets the limit of the relative voltage change time d(t) or queries the current 6-53
                          setting.
     :FLICker:DT[:STATe]  Turns ON/OFF judgment of the relative voltage change time d(t) or queries 6-53
                          the current setting.
     :FLICker:EDITion     Sets the IEC standard edition for flicker measurement or queries the current 6-54
                          setting.
     :FLICker:ELEMent<x>  Sets the target element flicker measurement or queries the current setting. 6-54
     :FLICker:FREQuency   Sets the target frequency for flicker measurement or queries the current 6-54
                          setting.
     :FLICker:INITialize  Initializes flicker measurement.      6-54
     :FLICker:INTerval    Sets the time per measurement of the short-term flicker value Pst or queries 6-54
                          the current setting.
     :FLICker:JUDGe       Finishes measurement of dmax caused by manual switching and performs 6-54
                          judgment.
     :FLICker:MEASurement Sets the flicker measurement method or queries the current setting. 6-54
     :FLICker:MOVe        Moves the observation period number for measurement of dmax caused by 6-55
                          manual switching.
     :FLICker:PLT?        Queries all settings related to the long-term flicker value Plt. 6-55
     :FLICker:PLT:LIMit   Sets the limit of the long-term flicker value Plt or queries the current setting. 6-55
     :FLICker:PLT:NVALue  Sets constant N for the equation used to compute the long-term flicker value 6-55
                          Plt or queries the current setting.
     :FLICker:PLT[:STATe] Turns ON/OFF judgment of the long-term flicker value Plt or queries the 6-55
                          current setting.
     :FLICker:PST?        Queries all settings related to the short-term flicker value Pst. 6-55
     :FLICker:PST:LIMit   Sets the limit for the short-term flicker value or queries the current setting. 6-55
     :FLICker:PST[:STATe] Turns ON/OFF judgment of the short-term flicker value Pst or queries the 6-55
                          current setting.
     :FLICker:P3D3        Sets the edition of IEC 61000-3-3 or queries the current setting. 6-55
     :FLICker:P4D15       Sets the edition of IEC 61000-4-15 or queries the current setting. 6-55
     :FLICker:RESet       Resets measured flicker data.         6-55
     :FLICker:STARt       Starts flicker measurement.           6-56
     :FLICker:STATe?      Queries the status of flicker measurement. 6-56
     :FLICker:TMAX?       Queries all settings related to Tmax. 6-56
```

## Page 6-8

```text
 6.1 List of Commands

   Command              Function                              Page
   :FLICker:TMAX:LIMit  Sets the limit of the Tmax or queries the current setting. 6-56
   :FLICker:TMAX[:STATe] Turns ON/OFF judgment of the Tmax or queries the current setting. 6-56
   :FLICker:UN?         Queries all settings related to rated voltage Un. 6-56
   :FLICker:UN:MODE     Sets the assignment method for rated voltage Un or queries the current 6-56
                        setting.
   :FLICker:UN:VALue    Sets the predefined value of rated voltage Un or queries the current setting. 6-56
   :FLICker:VOLTage     Sets the flicker target voltage or queries the current setting. 6-56
   HARMonics Group
   :HARMonics?          Queries all settings related to harmonic measurement. 6-57
   :HARMonics:FBANd     Sets the frequency bandwidth of the harmonic measurement or queries the 6-57
                        current setting.
   :HARMonics:IEC?      Queries all settings related to IEC harmonic measurement. 6-57
   :HARMonics:IEC:OBJect Sets the IEC harmonic measurement target or queries the current setting. 6-57
   :HARMonics:IEC:{UGRouping|IGRou Sets the {voltage|current} grouping of the IEC harmonic measurement or 6-57
   ping}                queries the current setting.
   :HARMonics:ORDer     Sets the maximum and minimum orders to be measured or queries the 6-57
                        current setting.
   :HARMonics:PLLSource Sets the PLL source or queries the current setting. 6-58
   :HARMonics:PLLWarning? Queries all settings related to the warning messages of the PLL source. 6-58
   :HARMonics:PLLWarning[:STATe] Sets whether to generate a warning message when the PLL source is not 6-58
                        applied or queries the current setting.
   :HARMonics:THD       Sets the equation used to calculate the THD (total harmonic distortion) or 6-58
                        queries the current setting.
   HCOPy Group
   :HCOPy? (Hard COPY)  Queries all settings related to the printing. 6-59
   :HCOPy:ABORt         Aborts printing or paper feeding.     6-59
   :HCOPy:AUTO?         Queries all settings related to the auto print. 6-59
   :HCOPy:AUTO:INTerval Sets the auto print interval or queries the current setting. 6-59
   :HCOPy:AUTO:{STARt|END} Sets the {start|stop} reservation time of the auto print or queries the current 6-59
                        setting.
   :HCOPy:AUTO[:STATe]  Turns ON/OFF the auto print or queries the current setting. 6-59
   :HCOPy:AUTO:SYNChronize Sets the synchronization mode of the auto print or queries the current 6-59
                        setting.
   :HCOPy:COMMent       Sets the comment displayed at the bottom of the screen or queries the 6-60
                        current setting.
   :HCOPy:DIRection     Sets the printer or queries the current setting. 6-60
   :HCOPy:EXECute       Executes printing.                    6-60
   :HCOPy:NETPrint?     Queries all settings related to the printing on the network printer. 6-60
   :HCOPy:NETPrint:COLor Turns ON/OFF color printing on the network printer or queries the current 6-60
                        setting.
   :HCOPy:NETPrint:FORMat Sets the printer description language for printing on a network printer or 6-60
                        queries the current setting.
   :HCOPy:PRINter?      Queries all settings related to printing on the built-in printer. 6-60
   :HCOPy:PRINter:FEED  Executes paper feeding of the built-in printer. 6-60
   :HCOPy:PRINter:FORMat Sets the contents to be printed on the built-in printer or queries the current 6-60
                        setting.
   :HCOPy:PRINter:LIST? Queries all settings related to the printing of the numeric data list on the built- 6-61
                        in printer.
   :HCOPy:PRINter:LIST:INFOrmation Sets whether to add setup parameters when printing the numeric data list on 6-61
                        the built-in printer or queries the current setting.
   :HCOPy:PRINter:LIST:NORMal? Queries all settings related to the printed items of the numeric data list using 6-61
                        the built-in printer.
   :HCOPy:PRINter:LIST[:NORMal]:A Collectively turns ON/OFF the output of all element functions when printing 6-61
   LL                   the numeric data list on the built-in printer.
   :HCOPy:PRINter:LIST[:NORMal]:{E Turns ON/OFF the output of {each element|ΣA|ΣB} when printing the numeric 6-61
   LEMent<x>|SIGMA|SIGMB} data list on the built-in printer.
   :HCOPy:PRINter:LIST[:NORMal]:PR Presets the output ON/OFF pattern of the element functions when printing 6-61
   ESet<x>              the numeric data list on the built-in printer.
   :HCOPy:PRINter:LIST[:NORMal]:<F urns ON/OFF the output of the function when printing the numerical data list 6-62
   unction>             using the built-in printer or queries the current setting.
```

## Page 6-9

```text
                                                      6.1 List of Commands

     Command              Function                              Page

     HOLD Group
     :HOLD                Sets the output data (display, communications, etc.) hold or queries the 6-63
                          current setting.
     IMAGe Group
     :IMAGe?              Queries all settings related to the saving of screen image data. 6-64
     :IMAGe:ABORt         Aborts the saving of the screen image data. 6-64
     :IMAGe:COLor         Sets the color tone of the screen image data to be saved or queries the 6-64
                          current setting.
     :IMAGe:COMMent       Sets the comment displayed at the bottom of the screen or queries the 6-64
                          current setting.
     :IMAGe:COMPression   Enables or disables the data compression of screen image data in BMP 6-64
                          format or queries the current setting.
     :IMAGe:EXECute       Saves the screen image data.          6-64
     :IMAGe:FORMat        Sets the format of the screen image data to be saved or queries the current 6-64
                          setting.
     :IMAGe:SAVE?         Queries all settings related to the saving of screen image data. 6-64
     :IMAGe:SAVE:ANAMing  Sets whether to automatically name the screen image data files to be saved 6-64
                          or queries the current setting.
     :IMAGe:SAVE:CDIRectory Changes the save destination directory for the screen image data. 6-64
     :IMAGe:SAVE:DRIVe    Sets the save destination drive of the screen image data. 6-65
     :IMAGe:SAVE:NAME     Sets the name of the file for saving the screen image data or queries the 6-65
                          current setting.
     :IMAGe:SEND?         Queries the screen image data.        6-65
     INPut Group
     :INPut?              Queries all settings related to the input element. 6-66
     [:INPut]:CFACtor     Sets the crest factor or queries the current setting. 6-66
     [:INPut]:CURRent?    Queries all settings related to the current measurement. 6-66
     [:INPut]:CURRent:AUTO? Queries the current auto range setting (ON/OFF) of all elements. 6-66
     [:INPut]:CURRent:AUTO[:ALL] Collectively turns ON/OFF the current auto range of all elements. 6-66
     [:INPut]:CURRent:AUTO:ELEMent Turns ON/OFF the current auto range of the element or queries the current 6-67
     <x>                  setting.
     [:INPut]:CURRent:AUTO:{SIGMA|SI Collectively turns ON/OFF the current auto range of all elements belonging 6-67
     GMB}                 to wiring unit {ΣA|ΣB}.
     [:INPut]:CURRent:MODE? Queries the current mode of all elements. 6-67
     [:INPut]:CURRent:MODE[:ALL] Collectively sets the current mode of all elements. 6-67
     [:INPut]:CURRent:MODE:ELEMent Sets the current mode of the element or queries the current setting. 6-67
     <x>
     [:INPut]:CURRent:MODE:{SIGMA|SI Collectively sets the current mode of all elements belonging to wiring unit 6-67
     GMB}                 {ΣA|ΣB}.
     [:INPut]:CURRent:RANGe? Queries the current ranges of all elements. 6-67
     [:INPut]:CURRent:RANGe[:ALL] Collectively sets the current ranges of all elements. 6-67
     [:INPut]:CURRent:RANGe:ELEMent Sets the current range of the element or queries the current setting. 6-68
     <x>
     [:INPut]:CURRent:RANGe:{SIGMA|S Collectively sets the current range of all elements belonging to wiring unit 6-68
     IGMB}                {ΣA|ΣB}.
     [:INPut]:CURRent:SRATio? Queries the current sensor scaling constants of all elements. 6-69
     [:INPut]:CURRent:SRATio[:ALL] Collectively sets the current sensor scaling constants of all elements. 6-69
     [:INPut]:CURRent:SRATio:ELEMent Sets the current sensor scaling constant of the element or queries the 6-69
     <x>                  current setting.
     [:INPut]:FILTer?     Queries all settings related to the filter. 6-69
     [:INPut]:FILTer:FREQuency? Queries the frequency filter settings of all elements. 6-69
     [:INPut]:FILTer:FREQuency[:ALL] Collectively sets the frequency filter of all elements. 6-69
     [:INPut]:FILTer:FREQuency:ELEMe Sets the frequency filter of the element or queries the current setting. 6-69
     nt<x>
     [:INPut]:FILTer:LINE? Queries the line filter settings of all elements. 6-69
     [:INPut]:FILTer[:LINE][:ALL] Collectively sets the line filters of all elements. 6-69
     [:INPut]:FILTer[:LINE]:ELEMent Sets the line filter of the element or queries the current setting. 6-69
     <x>
```

## Page 6-10

```text
 6.1 List of Commands

   Command              Function                              Page
   [:INPut]:INDependent Turns ON/OFF the independent setting of input elements or queries the 6-69
                        current setting.
   [:INPut]:MODUle?     Queries the input element type.       6-70
   [:INPut]:NULL        Turns ON/OFF the NULL function or queries the current setting. 6-70
   [:INPut]:POVer?      Queries the peak over information.    6-70
   [:INPut]:SCALing?    Queries all settings related to scaling. 6-70
   [:INPut]:SCALing:{VT|CT|SFACt Queries the {VT ratio|CT ratio|power factor} of all elements. 6-70
   or}?
   [:INPut]:SCALing:{VT|CT|SFACtor Collectively sets the {VT ratio|CT ratio|power factor} of all elements. 6-70
   }[:ALL]
   [:INPut]:SCALing:{VT|CT|SFACtor Sets the {VT ratio|CT ratio|power factor} of the element or queries the current 6-70
   }:ELEMent<x>         setting.
   [:INPut]:SCALing:STATe? Queries the scaling ON/OFF states of all elements. 6-70
   [:INPut]:SCALing[:STATe][:ALL] Collectively turns ON/OFF the scaling of all elements. 6-70
   [:INPut]:SCALing[:STATe]:ELEMen Turns ON/OFF the scaling of the element or queries the current setting. 6-71
   t<x>
   [:INPut]:SYNChronize? Queries the synchronization source of all elements. 6-71
   [:INPut]:SYNChronize[:ALL] Collectively sets the synchronization source of all elements. 6-71
   [:INPut]:SYNChronize:ELEMent<x> Sets the synchronization source of the element or queries the current setting. 6-71
   [:INPut]:SYNChronize:{SIGMA|SIG Collectively sets the synchronization source of all elements belonging to 6-71
   MB}                  wiring unit {ΣA|ΣB}.
   [:INPut]:VOLTage?    Queries all settings related to the voltage measurement. 6-71
   [:INPut]:VOLTage:AUTO? Queries the voltage auto range setting (ON/OFF) of all elements. 6-71
   [:INPut]:VOLTage:AUTO[:ALL] Collectively turns ON/OFF the voltage auto range of all elements. 6-71
   [:INPut]:VOLTage:AUTO:ELEMent Turns ON/OFF the voltage auto range of the element or queries the current 6-71
   <x>                  setting.
   [:INPut]:VOLTage:AUTO:{SIGMA|SI Collectively turns ON/OFF the voltage auto range of all elements belonging 6-71
   GMB}                 to wiring unit {ΣA|ΣB}.
   [:INPut]:VOLTage:MODE? Queries the voltage mode of all elements. 6-72
   [:INPut]:VOLTage:MODE[:ALL] Collectively sets the voltage mode of all elements. 6-72
   [:INPut]:VOLTage:MODE:ELEMent Sets the voltage mode of the element or queries the current setting. 6-72
   <x>
   [:INPut]:VOLTage:MODE:{SIGMA|SI Collectively sets the voltage mode of all elements belonging to wiring unit 6-72
   GMB}                 {ΣA|ΣB}.
   [:INPut]:VOLTage:RANGe? Queries the voltage ranges of all elements. 6-72
   [:INPut]:VOLTage:RANGe[:ALL] Collectively sets the voltage range of all elements. 6-72
   [:INPut]:VOLTage:RANGe:ELEMent Sets the voltage range of the element or queries the current setting. 6-72
   <x>
   [:INPut]:VOLTage:RANGe:{SIGMA|S Collectively sets the voltage range of all elements belonging to wiring unit 6-72
   IGMB}                {ΣA|ΣB}.
   [:INPut]:WIRing      Sets the wiring system or queries the current setting. 6-73
   INTEGrate Group
   :INTEGrate?          Queries all settings related to the integration. 6-74
   :INTEGrate:ACAL      Turns ON/OFF the auto calibration or queries the current setting. 6-74
   :INTEGrate:MODE      Sets the integration mode or queries the current setting. 6-74
   :INTEGrate:RESet     Resets the integrated value.          6-74
   :INTEGrate:RTIMe?    Queries the integration start and stop times for real-time integration mode. 6-74
   :INTEGrate:RTIMe:{STARt|END} Sets the integration {start|stop} time for real-time integration mode or queries 6-74
                        the current setting.
   :INTEGrate:STARt     Starts integration.                   6-74
   :INTEGrate:STATe?    Queries the integration condition.    6-74
   :INTEGrate:STOP      Stops integration.                    6-74
   :INTEGrate:TIMer<x>  Sets the integration timer time or queries the current setting. 6-75
```

## Page 6-11

```text
                                                      6.1 List of Commands

     Command              Function                              Page

     MEASure Group
     :MEASure?            Queries all settings related to the computation. 6-76
     :MEASure:AVERaging?  Queries all settings related to averaging. 6-76
     :MEASure:AVERaging:COUNt Sets the averaging coefficient or queries the current setting. 6-76
     :MEASure:AVERaging[:STATe] Turns ON/OFF averaging or queries the current setting. 6-76
     :MEASure:AVERaging:TYPE Sets the averaging type or queries the current setting. 6-77
     :MEASure:COMPensation? Queries all settings related to the compensation computation. 6-77
     :MEASure:COMPensation:EFFicien Turns ON/OFF the efficiency compensation or queries the current setting. 6-77
     cy
     :MEASure:COMPensation:V3A3 Turns ON/OFF the compensation for the two-wattmeter method or queries 6-77
                          the current setting.
     :MEASure:COMPensation:WIRing? Queries all settings related to the wiring compensation. 6-77
     :MEASure:COMPensation:WIRing:EL Sets the wiring compensation of the element or queries the current setting. 6-77
     EMent<x>
     :MEASure:DMeasure?   Queries all settings related to the delta computation. 6-77
     :MEASure:DMeasure[:SIGMA] Sets the delta computation mode for wiring unit ΣA or queries the current 6-78
                          setting.
     :MEASure:DMeasure:SIGMB Sets the delta computation mode for wiring unit ΣB or queries the current 6-78
                          setting.
     :MEASure:EFFiciency? Queries all settings related to the efficiency computation. 6-78
     :MEASure:EFFiciency:ETA<x> Sets the efficiency equation or queries the current setting. 6-78
     :MEASure:EFFiciency:UDEF<x> Sets the user-defined parameter used in the efficiency equation or queries 6-78
                          the current setting.
     :MEASure:FREQuency?  Queries all settings related to frequency measurement. 6-79
     :MEASure:FREQuency:ITEM<x> Sets the frequency measurement item or queries the current setting. 6-79
     :MEASure:FUNCtion<x>? Queries all settings related to user-defined functions. 6-79
     :MEASure:FUNCtion<x>:EXPRession Sets the equation of the user-defined function or queries the current setting. 6-79
     :MEASure:FUNCtion<x>[:STATe] Enables (ON) or Disables (OFF) the user-defined function or queries the 6-79
                          current setting.
     :MEASure:FUNCtion<x>:UNIT Sets the unit to be added to the computation result of the user-defined 6-79
                          function or queries the current setting.
     :MEASure:MHOLd       Enables (ON) or Disables (OFF) MAX HOLD function used in the user- 6-79
                          defined function or queries the current setting.
     :MEASure:PC?         Queries all settings related to the computation of Pc (Corrected Power). 6-79
     :MEASure:PC:IEC      Sets the equation used to compute Pc (Corrected Power) or queries the 6-80
                          current setting.
     :MEASure:PC:P<x>     Sets the parameter used to compute Pc (Corrected Power) or queries the 6-80
                          current setting.
     :MEASure:PHASe       Sets the display format of the phase difference or queries the current setting. 6-80
     :MEASure:SAMPling    Sets the sampling frequency or queries the current setting. 6-80
     :MEASure:SQFormula   Sets the equation used to compute S (apparent power) and Q (reactive 6-80
                          power) or queries the current setting.
     :MEASure:SYNChronize Sets the synchronized measurement mode or queries the current setting. 6-80
```

## Page 6-12

```text
 6.1 List of Commands

   Command              Function                              Page

   MOTor Group
   :MOTor?              Queries all settings related to the motor evaluation function. 6-81
   :MOTor:FILTer?       Queries all settings related to the input filter. 6-81
   :MOTor:FILTer[:LINE] Sets the line filter or queries the current setting. 6-81
   :MOTor:PM?           Queries all settings related to the motor output (Pm). 6-81
   :MOTor:PM:SCALing    Sets the scaling factor used for motor output computation or queries the 6-81
                        current setting.
   :MOTor:PM:UNIT       Sets the unit to add to the motor output computation result or queries the 6-81
                        current setting.
   :MOTor:POLE          Sets the motor’s number of poles or queries the current setting. 6-81
   :MOTor:SPEed?        Queries all settings related to the rotating speed. 6-81
   :MOTor:SPEed:AUTO    Turns ON/OFF the voltage auto range of the revolution signal input (analog 6-81
                        input format) or queries the current setting.
   :MOTor:SPEed:PRANge  Sets the range of the rotating speed (pulse input format) or queries the 6-82
                        current setting.
   :MOTor:SPEed:PULSe   Sets the pulse count of the revolution signal input (pulse input) or queries the 6-82
                        current setting.
   :MOTor:SPEed:RANGe   Sets the voltage range of the revolution signal input (analog input format) or 6-82
                        queries the current setting.
   :MOTor:SPEed:SCALing Sets the scaling factor for rotating speed computation or queries the current 6-82
                        setting.
   :MOTor:SPEed:TYPE    Sets the input type of the revolution signal input or queries the current 6-82
                        setting.
   :MOTor:SPEed:UNIT    Sets the unit to add to the rotating speed computation result or queries the 6-82
                        current setting.
   :MOTor:SSPeed(Sync SPeed source) Sets the frequency measurement source used to compute the synchronous 6-82
                        speed (SyncSp) or queries the current setting.
   :MOTor:SYNChronize   Sets the synchronization source used to compute the rotating speed and 6-82
                        torque or queries the current setting.
   :MOTor:TORQue?       Queries all settings related to the torque. 6-82
   :MOTor:TORQue:AUTO   Turns ON/OFF the voltage auto range of the torque signal input (analog input 6-83
                        format) or queries the current setting.
   :MOTor:TORQue:PRANge Sets the range of the torque (pulse input format) or queries the current 6-83
                        setting.
   :MOTor:TORQue:RANGe  Sets the voltage range of the torque signal input (analog input format) or 6-83
                        queries the current setting.
   :MOTor:TORQue:RATE?  Queries all settings related to the rated value of the torque signal (pulse input 6-83
                        format).
   :MOTor:TORQue:RATE:{UPPer|LOW Sets the rated value {upper limit|lower limit} of the torque signal (pulse input 6-83
   er}                  format) or queries the current setting.
   :MOTor:TORQue:SCALing Sets the scaling factor used for torque computation or queries the current 6-83
                        setting.
   :MOTor:TORQue:TYPE   Sets the input type of the torque signal input or queries the current setting. 6-83
   :MOTor:TORQue:UNIT   Sets the unit to add to the torque computation result or queries the current 6-83
                        setting.
   NUMeric Group
   :NUMeric?            Queries all settings related to the numeric data output. 6-84
   :NUMeric:CBCycle?    Queries all settings related to output of numeric list data of Cycle by Cycle 6-84
                        measurement.
   :NUMeric:CBCycle:END Sets the output end cycle of the numeric list data output by 6-84
                        :NUMeric:CBCycle:VALue? or queries the current setting.
   :NUMeric:CBCycle:ITEM Sets the numeric list data output items (function and element) of Cycle by 6-84
                        Cycle measurement or queries the current setting.
   :NUMeric:CBCycle:STARt Sets the output start cycle of the numeric list data output by 6-84
                        :NUMeric:CBCycle:VALue? or queries the current setting.
   :NUMeric:CBCycle:VALue? Queries the numeric list data from Cycle by Cycle measurement. 6-85
   :NUMeric:FLICker?    Queries all settings related to output of numeric data from flicker 6-85
                        measurement.
   :NUMeric:FLICker:COUNt? Queries the number of the measurement within the specified observation 6-85
                        period at which flicker measurement stops.
```

## Page 6-13

```text
                                                      6.1 List of Commands

     Command              Function                              Page
     :NUMeric:FLICker:FUNCtion? Queries all settings related to output of measured flicker data (variable 6-85
                          format).
     :NUMeric:FLICker:FUNCtion:CLEar Clears (sets to NONE) the output items of measured flicker data (variable 6-86
                          format).
     :NUMeric:FLICker:FUNCtion:DELe Deletes the output items of measured flicker data (variable format). 6-86
     te
     :NUMeric:FLICker:FUNCtion:ITEM Sets output items (function, element, and observation period) of measured 6-86
     <x>                  flicker data (variable format) or queries the current setting.
     :NUMeric:FLICker:FUNCtion:NUMb Sets the number of measured flicker data output by “:NUMeric:FLICker:FUN 6-87
     er                   Ction:VALue?” or queries the current setting.
     :NUMeric:FLICker:FUNCtion:VAL Queries the measured flicker data (variable format). 6-87
     ue?
     :NUMeric:FLICker:INFOrmation? Queries all settings related to output of flicker judgment results (variable 6-87
                          format).
     :NUMeric:FLICker:INFOrmation:CL Clears (sets to NONE) the output items of flicker judgment results (variable 6-88
     Ear                  format).
     :NUMeric:FLICker:INFOrmation:DE Deletes the output items of flicker judgment results (variable format). 6-88
     Lete
     :NUMeric:FLICker:INFOrmation:IT Sets the output items (function, element, and observation period) of flicker 6-88
     EM<x>                judgment results (variable format) or queries the current setting.
     :NUMeric:FLICker:INFOrmation:NU Sets the number of flicker judgment results output by “:NUMeric:FLICker:INF 6-89
     Mber                 Ormation:VALue?” or queries the current setting.
     :NUMeric:FLICker:INFOrmation:VA Queries the judgment results (variable format). 6-89
     Lue?
     :NUMeric:FLICker:JUDGement? Queries the judgment results (fixed format). 6-90
     :NUMeric:FLICker:PERiod? Queries the observation period number currently being measured during 6-90
                          flicker measurement.
     :NUMeric:FLICker:VALue? Queries the measured flicker data (fixed format). 6-91
     :NUMeric:FORMat      Sets the format of the numeric data that is transmitted by 6-91
                          “:NUMeric[:NORMal]:VALue?” or “:NUMeric:LIST:VALue?” or queries the
                          current setting.
     :NUMeric:HOLD        Sets whether to hold (ON) or release (OFF) all the numeric data or queries 6-92
                          the current setting.
     :NUMeric:LIST?       Queries all settings related to the numeric list data output of harmonic 6-92
                          measurement.
     :NUMeric:LIST:CLEar  Clears the output items of the numeric list data of harmonic measurement (set 6-92
                          to “NONE”).
     :NUMeric:LIST:DELete Deletes the output items of the numeric list data of harmonic measurement. 6-93
     :NUMeric:LIST:ITEM<x> Sets the output items (function elements) of the numeric list data of harmonic 6-93
                          measurement or queries the current setting.
     :NUMeric:LIST:NUMber Sets the number of the numeric list data that is transmitted by 6-93
                          “:NUMeric:LIST:VALue?” or queries the current setting.
     :NUMeric:LIST:ORDer  Sets the maximum output order of the numeric list data of harmonic 6-93
                          measurement or queries the current setting.
     :NUMeric:LIST:PRESet Sets the output items of harmonic measurement numeric list data to a preset 6-93
                          pattern.
     :NUMeric:LIST:SELect Sets the output component of the numeric list data of harmonic measurement 6-94
                          or queries the current setting.
     :NUMeric:LIST:VALue? Queries the numeric list data of harmonic measurement. 6-94
     :NUMeric:NORMal?     Queries all settings related to the numeric data output. 6-95
     :NUMeric[:NORMal]:CLEar Clears the numeric data output item (sets “NONE”). 6-95
     :NUMeric[:NORMal]:DELete Deletes the output items of numeric data. 6-95
     :NUMeric[:NORMal]:ITEM<x> Sets the numeric data output items (function, element, and harmonic order) 6-95
                          or queries the current setting.
     :NUMeric[:NORMal]:NUMber Sets the number of the numeric data that is transmitted by 6-95
                          “:NUMeric[:NORMal]:VALue?” or queries the current setting.
     :NUMeric[:NORMal]:PRESet Presets the output item pattern of numeric data. 6-95
     :NUMeric[:NORMal]:VALue? Queries the numeric data.         6-96
     RATE Group
     :RATE                Sets the data update interval or queries the current setting. 6-102
```

## Page 6-14

```text
 6.1 List of Commands

   Command              Function                              Page

   STATus Group
   :STATus?             Queries all settings related to the communication status function. 6-103
   :STATus:CONDition?   Queries the contents of the condition register. 6-103
   :STATus:EESE(Extended Event Sets the extended event enable register or queries the current setting. 6-103
   Status Enable register)
   :STATus:EESR?(Extended Event Queries the content of the extended event register and clears the register. 6-103
   Status Register)
   :STATus:ERRor?       Queries the error code and message information (top of the error queue). 6-103
   :STATus:FILTer<x>    Sets the transition filter or queries the current setting. 6-103
   :STATus:QENable      Sets whether to store messages other than errors to the error queue (ON/ 6-103
                        OFF) or queries the current setting.
   :STATus:QMESsage     Sets whether to attach message information to the response to the 6-103
                        “STATus:ERRor?” query (ON/OFF) or queries the current setting.
   :STATus:SPOLl? (Serial Poll) Executes serial polling.      6-104
   STORe Group
   :STORe?              Queries all settings related to store and recall. 6-105
   :STORe:COUNt         Sets the store count or queries the current setting. 6-105
   :STORe:DIRection     Sets the store destination or queries the current setting. 6-105
   :STORe:FILE?         Queries all settings related to the saving of the stored data. 6-105
   :STORe:FILE:ANAMing  Sets whether to automatically name the files when saving the stored data or 6-105
                        queries the current setting.
   :STORe:FILE:COMMent  Sets the comment to be added to the file when saving the stored data or 6-105
                        queries the current setting.
   :STORe:FILE:NAME     Sets the name of the file when saving the stored data or queries the current 6-105
                        setting.
   :STORe:FILE:TYPE     Sets the data format when saving the stored data or queries the current 6-105
                        setting.
   :STORe:INTerval      Sets the store interval or queries the current setting. 6-106
   :STORe:ITEM          Sets the stored item or queries the current setting. 6-106
   :STORe:MEMory?       Queries all settings related to the storage memory. 6-106
   :STORe:MEMory:ALERt  Sets whether to display a confirmation message when clearing the storage 6-106
                        memory or queries the current setting.
   :STORe:MEMory:CONVert:ABORt Abort converting the stored data from the memory to the file. 6-106
   :STORe:MEMory:CONVert:EXECute Executes the converting of the stored data from the memory to the file. 6-106
   :STORe:MEMory:INITialize Executes the initialization of the storage memory. 6-106
   :STORe:MODE          Sets the data storage/recall or queries the current setting. 6-106
   :STORe:NUMeric?      Queries all settings related to the storage of numeric data. 6-107
   :STORe:NUMeric:NORMal? Queries all settings related to the stored items of numeric data. 6-107
   :STORe:NUMeric[:NORMal]:ALL Collectively turns ON/OFF the output of all element functions when storing 6-107
                        the numerical data.
   :STORe:NUMeric[:NORMal]:{ELEMen Turns ON/OFF the output of {each element|ΣA|ΣB} when storing the numeric 6-107
   t<x>|SIGMA|SIGMB}    data.
   :STORe:NUMeric[:NORMal]:PRESet Presets the output ON/OFF pattern of the element function for storing the 6-107
   <x>                  numeric data.
   :STORe:NUMeric[:NORMal]:<Functi Turns ON/OFF the output of the function when storing the numerical data or 6-107
   on>                  queries the current setting.
   :STORe:RECall        Sets the data number to be recalled or queries the current setting. 6-108
   :STORe:RTIMe?        Queries the store reservation time for real-time store mode. 6-108
   :STORe:RTIMe:{STARt|END} Sets the store {start|stop} reservation date/time for real-time store mode or 6-108
                        queries the current setting.
   :STORe:SMODe         Sets the store mode or queries the current setting. 6-108
   :STORe:STARt         Starts the data store operation.      6-108
   :STORe:STOP          Stops the data storage operation.     6-108
   :STORe:WAVE?         Queries all settings related to the storage of waveform display data. 6-108
   :STORe:WAVE:ALL      Collectively turns ON/OFF the output of all waveforms when storing 6-108
                        waveform display data.
   :STORe:WAVE:{U<x>|I<x>|SPEed|TO Turns ON/OFF the output of the waveform when storing the waveform 6-108
   RQue}                display data or queries the current setting.
```

## Page 6-15

```text
                                                      6.1 List of Commands

     Command              Function                              Page

     SYSTem Group
     :SYSTem?             Queries all settings related to the system. 6-109
     :SYSTem:CLOCk?       Sets all date/time related settings or queries the current setting. 6-109
     :SYSTem:CLOCk:DISPlay Turns ON/OFF the date/time display or queries the current setting. 6-109
     :SYSTem:CLOCk:SNTP?  Sets all SNTP-based date/time related settings or queries the current setting. 6-109
     :SYSTem:CLOCk:SNTP[:EXECute] Sets the date/time via SNTP.  6-109
     :SYSTem:CLOCk:SNTP:GMTTime Sets the difference from Greenwich Mean Time or queries the current setting. 6-109
     :SYSTem:CLOCk:TYPE   Sets the date/time setting method or queries the current setting. 6-109
     :SYSTem:DATE         Sets the date or queries the current setting. 6-109
     :SYSTem:ECLear       Clears the error message displayed on the screen. 6-109
     :SYSTem:FONT         Sets the display font or queries the current setting. 6-109
     :SYSTem:KLOCk        Turns ON/OFF the key lock or queries the current setting. 6-110
     :SYSTem:LANGuage?    Queries all settings related to the display language. 6-110
     :SYSTem:LANGuage:MENU Sets the menu language or queries the current setting. 6-110
     :SYSTem:LANGuage:MESSage Sets the message language or queries the current setting. 6-110
     :SYSTem:LCD?         Queries all settings related to the LCD monitor. 6-110
     :SYSTem:LCD:BRIGhtness Sets the brightness of the LCD monitor or queries the current setting. 6-110
     :SYSTem:LCD:COLor?   Queries all settings related to the display colors of the LCD monitor. 6-110
     :SYSTem:LCD:COLor:GRAPh? Queries all settings related to the display colors of the graphic items. 6-110
     :SYSTem:LCD:COLor:GRAPh:{BACKg Sets the display color of the {background|graticule|cursor|voltage 6-110
     round|GRATicule|CURSor|U<x>|I waveform|current waveform} or queries the current setting.
     <x>}
     :SYSTem:LCD:COLor:GRAPh:MODE Sets the display color mode of the graphic items or queries the current 6-110
                          setting.
     :SYSTem:LCD:COLor:TEXT? Queries all settings related to the display colors of the text items. 6-111
     :SYSTem:LCD:COLor:TEXT:{LETTer| Sets the display color of the {text (Menu Fore)|menu background (Menu 6-111
     BACKground|BOX|SUB|SELected} Back)|selected menu (Select Box)|pop-up menu (Sub Menu)|selected key
                          (Selected Key)} or queries the current setting.
     :SYSTem:LCD:COLor:TEXT:MODE Sets the display color mode of the text items or queries the current setting. 6-111
     :SYSTem:SLOCk        Sets whether to continue the SHIFT key ON state or queries the current 6-111
                          setting.
     :SYSTem:TIME         Sets the time or queries the current setting. 6-111
     :SYSTem:USBKeyboard  Sets the USB keyboard type (language) or queries the current setting. 6-111
     WAVeform Group
     :WAVeform?           Queries all settings related to the output of waveform display data. 6-112
     :WAVeform:BYTeorder  Sets the output byte order of the waveform display data (FLOAT format) that 6-112
                          is transmitted by “:WAVeform:SEND?” or queries the current setting.
     :WAVeform:END        Sets the output end point of the waveform display data that is transmitted by 6-112
                          “:WAVeform:SEND?” or queries the current setting.
     :WAVeform:FORMat     Sets the format of the waveform display data that is transmitted by 6-112
                          “:WAVeform:SEND?” or queries the current setting.
     :WAVeform:HOLD       Sets whether to hold (ON) or release (OFF) all the waveform display data or 6-112
                          queries the current setting.
     :WAVeform:LENGth?    Queries the total number of points of the waveform specified by 6-112
                          :WAVeform:TRACe.
     :WAVeform:SEND?      Queries the waveform display data specified by “:WAVeform:TRACe”. 6-113
     :WAVeform:SRATe?     Queries the sample rate of the retrieved waveform. 6-113
     :WAVeform:STARt      Sets the output start point of the waveform display data that is transmitted by 6-113
                          “:WAVeform:SEND?” or queries the current setting.
     :WAVeform:TRACe      Sets the target waveform for “:WAVeform:SEND?” or queries the current 6-113
                          setting.
     :WAVeform:TRIGger?   Queries the trigger position of the retrieved waveform. 6-113
```

## Page 6-16

```text
 6.1 List of Commands

   Command              Function                              Page

   Common Command Group
   *CAL?(CALibrate)     Executes zero calibration (zero-level compensation, same operation as 6-114
                        pressing CAL (SHIFT+SINGLE)) and queries the result.
   *CLS(CLear Status)   Clears the standard event register, extended event register, and error queue. 6-114
   *ESE
   (standard Event Status Enable Sets the standard event enable register or queries the current setting. 6-114
   register)
   *ESR?(standard Event Status Queries the standard event register and clears the register. 6-114
   Register)
   *IDN?(IDeNtify)      Queries the instrument model.         6-114
   *OPC(OPeration Complete) Sets bit 0 (OPC bit) of the standard event register to 1 upon the completion 6-115
                        of the specified overlap command.
   *OPC?(OPeration Complete) ASCII code “1” is returned when the specified overlap command is 6-115
                        completed.
   *OPT?(OPTion)        Queries the installed options.        6-115
   *PSC(Power-on Status Clear) Sets whether to clear the registers below at power on or queries the current 6-115
                        setting. The register is cleared when the value rounded to an integer is a
                        non-zero value.
   *RST(ReSeT)          Initializes the settings.             6-115
   *SRE(Service Request Enable Sets the service request enable register or queries the current setting. 6-115
   register)
   *STB?(STatus Byte)   Queries the status byte register.     6-116
   *TRG(TRiGger)        Executes single measurement (the same operation as when SINGLE is 6-116
                        pressed).
   *TST?(TeST)          Performs a self-test and queries the result. 6-116
   *WAI(WAIt)           Holds the subsequent command until the completion of the specified overlap 6-116
                        operation.
```

## Page 6-17

### Section introduction
```text
     6.2    ACQuisition    Group

   The commands in this group deal with output of the waveform sampling data (acquisition data).
   There are no front panel keys that correspond to the commands in this group.
   The commands in this group are valid only when the advanced computation function (/G6 option) is installed.
```
### Left column
```text
   :ACQuisition?
   Function Queries all settings related to the output of the
         waveform sampling data.
   Syntax :ACQuisition?
   Example :ACQUISITION? -> :ACQUISITION:
         TRACE U1;FORMAT ASCII;START 0;
         END 199999;HOLD 0

   :ACQuisition:BYTeorder
   Function Sets the output byte order of the waveform
         sampling data (FLOAT format) that is transmitted
         by “:ACQuisition:SEND?” or queries the
         current setting.
   Syntax :ACQuisition:BYTeorder {LSBFirst|
         MSBFirst}
         :ACQuisition:BYTeorder?
   Example :ACQUISITION:BYTEORDER LSBFIRST
         :ACQUISITION:BYTEORDER? ->
         :ACQUISITION:BYTEORDER LSBFIRST
   Description This value is valid when
         “:ACQuisition:FORMat” is set to FLOat.
   :ACQuisition:END
   Function Sets the output end point of the waveform
         display data that is transmitted by
         “:ACQuisition:SEND?” or queries the current
         setting.
   Syntax :ACQuisition:END {<NRf>}
         :ACQuisition:END?
         <NRf> = 0 to 3999999
   Example :ACQUISITION:END 199999
         :ACQUISITION:END? -> :ACQUISITION:END
         199999
   Description Set the point in the range up to (the total
         number of data points – 1). The total
         number of data points can be queried using
         “:ACQuisition:LENGth?.”
```
### Right column
```text
 :ACQuisition:FORMat
 Function Sets the format of the waveform sampling data
       that is transmitted by “:ACQuisition:SEND?”
       or queries the current setting.
 Syntax :ACQuisition:FORMat {ASCii|FLOat}
       :ACQuisition:FORMat?
 Example :ACQUISITION:FORMAT FLOAT
       :ACQUISITION:FORMAT? ->
       :ACQUISITION:FORMAT FLOAT
 Description For the differences in the waveform sampling
       data output due to the format setting, see the
       description for “:ACQuisition:SEND?.”
 :ACQuisition:HOLD
 Function Sets whether to hold (ON) or release (OFF)
       all the waveform sampling data or queries the
       current setting.
 Syntax :ACQuisition:HOLD {<Boolean>}
       :ACQuisition:HOLD?
 Example :ACQUISITION:HOLD ON
       :ACQUISITION:HOLD? ->
       :ACQUISITION:HOLD 1
 Description • This command is valid when the measurement
        mode is set to MATH or FFT. Otherwise, an
        error occurs.
       • When “:ACQuisition:HOLD” is turned ON,
        this instrument stops sampling the waveform
        sampling data and holds all of the waveform
        sampling data at that point internally. Be sure
        to set :ACQuisition:HOLD to ON before
        executing “:ACQuisition:SEND?.”
       • For example, if you wish to retrieve the
        waveform sampling data of U1 and I1 at the
        same point, do the following:
        :ACQuisition:HOLD ON
        :ACQuisition:TRACe U1
        :ACQuisition:SEND?
        (Receive the waveform sampling data of U1)
        :ACQuisition:TRACe I1
        :ACQuisition:SEND?
        (Receive the waveform sampling data of I1)
        :ACQuisition:HOLD OFF
       • To retrieve new waveform sampling data, set
        :ACQuisition:HOLD to OFF to resume
        sampling, and then set :ACQuisition:HOLD
        to ON again.
```

## Page 6-18

### Left column
```text
 6.2 ACQuisition Group

 :ACQuisition:LENGth?
 Function Queries the total number of points of
       the waveform sampling specified by
       “:ACQuisition:TRACe.”
 Syntax :ACQuisition:LENGth?
 Example :ACQUISITION:LENGTH? -> 100000
 Description • When the measurement mode is MATH, the
        number of data is determined by the data
        update interval (:RATE) setting.
        length = rate(sec) × 200000
       • When the measurement mode is FFT, the
        number of data is determined by the setting
        for the number of FFT computation points
        (:DISPlay:FFT:POINt) as follows:
        (1) When “:ACQuisition:TRACe” is
        FFT<x>
           length = point/2+1 = 10001 or 100001
        (2) When “:ACQuisition:TRACe” is not
        FFT<x>
           length = point = 20000 or 200000
       • In a mode other than MATH or FFT, an error
        occurs since there is no acquisition data, and 0
        is returned.
 :ACQuisition:SEND?
 Function Queries the waveform sampling data specified by
       “:ACQuisition:TRACe.”
 Syntax :ACQuisition:SEND?
 Example • When “:ACQuisition:FORMat” is set to
        {ASCii}
        :ACQUISITION:SEND? ->
        <NR3>,<NR3>,...
       • When “:ACQuisition:FORMat” is set to
        {FLOat}
        :ACQUISITION:SEND? -> #8 (number of
        bytes, 8 digits)(data byte sequence)
 Description • The format of the waveform sampling data
        that is output varies depending on the
        “:ACQuisition:FORMat” setting as follows:
        (1) When “ASCii” is specified
           The physical value is output in the <NR3>
        format. The data of each point is delimited by a
        comma.
        (2) When “FLOat” is specified
           The physical value is output in IEEE
        single-precision floating point (4-byte) format.
           The output byte order of the data of
           each point follows the order that is set
           using the “:ACQuisition:BYTeorder”
           command.
       • This instrument outputs the waveform
        sampling data in the range specified by
        “:ACQuisition:{STARt|END}.” However,
        data exceeding the waveform sampling data
        range, 0 to (the total number of data points – 1),
        is not output.
```
### Right column
```text
       • This command is valid when the measurement
        mode is set to MATH or FFT and the waveform
        sampling data is held inside this instrument
        (:ACQuisition:HOLD ON). Otherwise, an
        error occurs, because there is no waveform
        sampling data. The output is as follows:
        (1) When “ASCii” is specified
           Outputs NAN.
        (2) When “FLOat” is specified
           Outputs #800000000.
 :ACQuisition:SRATe?
 Function Queries the sampling rate of the retrieved data
 Syntax :ACQuisition:SRATe?
 Example :ACQUISITION:SRATE? -> 195.312E+03
 Description This command is valid when the measurement
       mode is set to MATH or FFT. Otherwise, an
       error occurs (returns NAN), because there is no
       waveform sampling data.

 :ACQuisition:STARt
 Function Sets the output start point of the waveform
       display data that is transmitted by
       “:ACQuisition:SEND?” or queries the current
       setting.
 Syntax :ACQuisition:STARt {<NRf>}
       :ACQuisition:STARt?
       <NRf> = 0 to 3999999
 Example :ACQUISITION:START 0
       :ACQUISITION:START? ->
       :ACQUISITION:START 0
 Description Set the point in the range up to (the total
       number of data points – 1). The total
       number of data points can be queried using
       “:ACQuisition:LENGth?.”
 :ACQuisition:TRACe
 Function Sets the target trace of “:ACQuisition:SEND?”
       or queries the current setting.
 Syntax :ACQuisition:TRACe {U<x>|I<x>|
       SPEed|TORQue|MATH<x>|FFT<x>}
       :ACQuisition:TRACe?
       <x> of U<x>, I<x> = 1 to 4 (element)
       <x> of MATH<x> = 1 to 2 (MATH)
       <x> of FFT<x> = 1 or 2 (FFT)
 Example :ACQUISITION:TRACE U1
       :ACQUISITION:TRACE? ->
       :ACQUISITION:TRACE U1
 Description {SPEed|TORQue} are valid only on models with
       the motor evaluation function (/MTR option).
```

## Page 6-19

### Section introduction
```text
     6.3    AOUTput     Group

   The commands in this group deal with the D/A output.
   You can make the same settings and inquiries as when the “D/A Output Items” menu of MISC on the front panel is
   used.
   However, the commands in this group are valid only when the D/A output (/DA option) is installed.
                                           RATE16 100.0E+00,-100.0E+00;
```
### Left column
```text
   :AOUTput?
   Function Queries all settings related to the D/A output.
   Syntax :AOUTput?
   Example :AOUTPUT? -> Same as the response to
         “:AOUTput:NORMal?”

   :AOUTput:NORMal?
   Function Queries all settings related to the D/A output.
   Syntax :AOUTput:NORMal?
   Example :AOUTPUT:NORMAL? -> :AOUTPUT:
         NORMAL:CHANNEL1 U,1,TOTAL;
         CHANNEL2 I,1,TOTAL;
         CHANNEL3 P,1,TOTAL;
         CHANNEL4 S,1,TOTAL;
         CHANNEL5 Q,1,TOTAL;
         CHANNEL6 LAMBDA,1,TOTAL;
         CHANNEL7 PHI,1,TOTAL;CHANNEL8 FU,1;
         CHANNEL9 FI,1;CHANNEL10 NONE;
         CHANNEL11 NONE;CHANNEL12 NONE;
         CHANNEL13 NONE;CHANNEL14 NONE;
         CHANNEL15 NONE;CHANNEL16 NONE;
         CHANNEL17 NONE;CHANNEL18 NONE;
         CHANNEL19 NONE;CHANNEL20 NONE;
         MODE1 FIXED;MODE2 FIXED;
         MODE3 FIXED;MODE4 FIXED;
         MODE5 FIXED;MODE6 FIXED;
         MODE7 FIXED;MODE8 FIXED;
         MODE9 FIXED;MODE10 FIXED;
         MODE11 FIXED;MODE12 FIXED;
         MODE13 FIXED;MODE14 FIXED;
         MODE15 FIXED;MODE16 FIXED;
         MODE17 FIXED;MODE18 FIXED;
         MODE19 FIXED;MODE20 FIXED;
         RATE1 100.0E+00,-100.0E+00;
         RATE2 100.0E+00,-100.0E+00;
         RATE3 100.0E+00,-100.0E+00;
         RATE4 100.0E+00,-100.0E+00;
         RATE5 100.0E+00,-100.0E+00;
         RATE6 100.0E+00,-100.0E+00;
         RATE7 100.0E+00,-100.0E+00;
         RATE8 100.0E+00,-100.0E+00;
         RATE9 100.0E+00,-100.0E+00;
         RATE10 100.0E+00,-100.0E+00;
         RATE11 100.0E+00,-100.0E+00;
         RATE12 100.0E+00,-100.0E+00;
         RATE13 100.0E+00,-100.0E+00;
         RATE14 100.0E+00,-100.0E+00;
         RATE15 100.0E+00,-100.0E+00;
```
### Right column
```text
       RATE17 100.0E+00,-100.0E+00;
       RATE18 100.0E+00,-100.0E+00;
       RATE19 100.0E+00,-100.0E+00;
       RATE20 100.0E+00,-100.0E+00;
       IRTIME 1,0,0

 :AOUTput[:NORMal]:CHANnel<x>
 Function Sets the D/A output items (function, element, and
       harmonic order) or queries the current setting.
 Syntax :AOUTput[:NORMal]:CHANnel<x> {NONE|
       <Function>,<Element>,<Order>}
       :AOUTput[:NORMal]:CHANnel<x>?
       <x> = 1 to 20 (output channel)
       NONE = No output item
       <Function> = {U|I|P|S|Q|...}(See the
       function selection list (1) of “DISPlay group” on
       page 6-44.)
       <Element> = {<NRf>|SIGMa|SIGMB} (<NRf>
       = 1 to 4)
       <Order> = {TOTal|DC|<NRf>} (<NRf> = 1 to
       100)
 Example :AOUTPUT:NORMAL:CHANNEL1 U,1,TOTAL
       :AOUTPUT:NORMAL:CHANNEL1? ->
       :AOUTPUT:NORMAL:CHANNEL1 U,1,TOTAL
 Description • If <Element> is omitted, element 1 is set.
       • If <Order> is omitted, TOTal is set.
       • <Element> or <Order> is omitted from
         response to functions that do not need them.
 :AOUTput[:NORMal]:IRTime
 Function Sets the rated integration time for the D/A output
       of integrated values or queries the current setting.
 Syntax :AOUTput[:NORMal]:IRTime {<NRf>,
       <NRf>,<NRf>}
       :AOUTput[:NORMal]:IRTime?
       {<NRf>, <NRf>, <NRf>} = 0, 0, 0 to 10000, 0, 0
       1st <NRf> = 0 to 10000 (hour)
       2nd <NRf> = 0 to 59 (minute)
       3rd <NRf> = 0 to 59 (second)
 Example :AOUTPUT:NORMAL:IRTIME 1,0,0
       :AOUTPUT:NORMAL:IRTIME? ->
       :AOUTPUT:NORMAL:IRTIME 1,0,0
```

## Page 6-20

### Left column
```text
 6.3 AOUTput Group

 :AOUTput[:NORMal]:MODE<x>
 Function Sets the method of setting the rated value for the
       D/A output items or queries the current setting.
 Syntax :AOUTput[:NORMal]:MODE<x> {FIXed|
       MANual}
       :AOUTput[:NORMal]:MODE<x>?
       <x> = 1 to 20 (output channel)
 Example :AOUTPUT:NORMAL:MODE1 FIXED
       :AOUTPUT:NORMAL:MODE1? ->
       :AOUTPUT:NORMAL:MODE1 FIXED
 :AOUTput[:NORMal]:RATE<x>
 Function Manually sets the rated maximum and minimum
       values for the D/A output items or queries the
       current setting.
 Syntax :AOUTput[:NORMal]:MODE<x> {<NRf>,
       <NRf>}
       :AOUTput[:NORMal]:MODE<x>?
       <x> = 1 to 20 (output channel)
       <NRf> = –9.999E+30 to 9.999E+30 (rated value)
 Example :AOUTPUT:NORMAL:RATE1 100,-100
       :AOUTPUT:NORMAL:RATE1? ->
       :AOUTPUT:NORMAL:
       RATE1 100.0E+00,-100.0E+00
 Description • Set the maximum value and then the minimum
        value.
       • This setting is valid when the
        method of setting the rated value
        (:AOUTput[:NORMal]:MODE<x>) is set to
        FIXed.
```

## Page 6-21

### Section introduction
```text
     6.4    CBCycle    Group

   The CBCycle group contains commands related to Cycle by Cycle measurement functions.
   These commands allow you to enter and query the same settings that are available under ITEM in the “CbyC Items”
   menu and under FORM in the “CbyC Form” menu on the front panel.
```
### Left column
```text
   :CBCycle?
   Function Queries all settings related to the Cycle by Cycle
         measurement function.
   Syntax :CBCycle?
   Example :CBCYCLE? -> :CBCYCLE:SYNCHRONIZE:
         SOURCE U1;SLOPE RISE;:CBCYCLE:
         TRIGGER:MODE AUTO;SOURCE U1;
         SLOPE RISE;LEVEL 0.0;:CBCYCLE:
         COUNT 100;TIMEOUT 10;FILTER:LINE:
         ELEMENT1 50.0E+03;
         ELEMENT2 50.0E+03;
         ELEMENT3 50.0E+03;ELEMENT4 50.0E+03
   :CBCycle:COUNt
   Function Sets the number of cycles for Cycle by Cycle
         measurement or queries the current setting.
   Syntax :CBCycle:COUNt {<NRf>}
         :CBCycle:COUNt?
         <NRf> = 1 to 3000 (number of measured cycles)
   Example :CBCYCLE:COUNT 100
         :CBCYCLE:COUNT? ->
         :CBCYCLE:COUNT 100
   :CBCycle:DISPlay?
   Function Queries all settings related to the Cycle by Cycle
         display.
   Syntax :CBCycle:DISPlay?
   Example :CBCYCLE:DISPLAY? ->
         :CBCYCLE:DISPLAY:ITEM1 FREQ;
         ITEM2 U,1;ITEM3 I,1;ITEM4 P,1;
         ITEM5 S,1;CURSOR 1

   :CBCycle:DISPlay:CURSor
   Function Sets the cursor position of the Cycle by Cycle
         display or queries the current setting.
   Syntax :CBCycle:DISPlay:CURSor {<NRf>}
         :CBCycle:DISPlay:CURSor?
         <NRf> = 1 to 3000 (cursor position)
   Example :CBCYCLE:DISPLAY:CURSOR 1
         :CBCYCLE:DISPLAY:CURSOR? ->
         :CBCYCLE:DISPLAY:CURSOR 1
   Description • Specifies the cursor position by the cycle
          number.
         • You can make the same setting or query
          with the “:DISPlay:CBCycle:CURSor”
          command.
```
### Right column
```text
 :CBCycle:DISPlay:ITEM<x>
 Function Sets the displayed items (function and element)
       of the Cycle by Cycle display or queries the
       current setting.
 Syntax :CBCycle:DISPlay:
       ITEM<x> {<Function>,<Element>}
       :CBCycle:DISPlay:ITEM<x>?
       <x> = 1 to 5 (item number)
       <Function> = {FREQ|U|I|P|S|Q|LAMBda|
       SPEed|TORQue|PM}
       <Element> = {<NRf>|SIGMa|SIGMB} (<NRf>
        = 1 to 4)
 Example :CBCYCLE:DISPLAY:ITEM1 U,1
       :CBCYCLE:DISPLAY:ITEM1? ->
       :CBCYCLE:DISPLAY:ITEM1 U,1
 Description • When <Function> = {FREQ|SPEed|
        TORQue|PM}, <Element> need not be
        specified.
        <Element> is omitted from the response.
       • When <Element> is omitted, Element 1 is set.
       • {SPEed|TORQue|PM} is only valid on models
        with the motor evaluation function (/MTR
        option).
       • You can make the same setting or query
        with the “:DISPlay:CBCycle:ITEM<x>”
        command.
 :CBCycle:DISPlay:PAGE
 Function Sets the number of the displayed page of the
       Cycle by Cycle display or queries the current
       setting.
 Syntax :CBCycle:DISPlay:PAGE {<NRf>}
       :CBCycle:DISPlay:PAGE?
       <NRf> = 1 to 150 (page number)
 Example :CBCYCLE:DISPLAY:PAGE 1
       :CBCYCLE:DISPLAY:PAGE? ->
       :CBCYCLE:DISPLAY:PAGE 1
 Description • When a page number is set, the cursor moves
        to the top of the specified page.
       • You can make the same setting or query
        with the “:DISPlay:CBCycle:CURSor”
        command.
```

## Page 6-22

### Left column
```text
 6.4 CBCycle Group

 :CBCycle:FILTer?
 Function Queries all settings related to the filter for Cycle
       by Cycle measurement.
 Syntax :CBCycle:FILTer?
 Example :CBCYCLE:FILTER? ->
       :CBCYCLE:FILTER:LINE:
       ELEMENT1 50.0E+03;
       ELEMENT2 50.0E+03;
       ELEMENT3 50.0E+03;ELEMENT4 50.0E+03
 :CBCycle:FILTer:LINE?
 Function Queries all settings related to the line filter for
       Cycle by Cycle measurement.
 Syntax :CBCycle:FILTer:LINE?
 Example :CBCYCLE:FILTER:LINE? ->
       :CBCYCLE:FILTER:LINE:
       ELEMENT1 50.0E+03;
       ELEMENT2 50.0E+03;
       ELEMENT3 50.0E+03;ELEMENT4 50.0E+03

 :CBCycle:FILTer[:LINE][:ALL]
 Function Collectively sets the line filters of all elements for
       Cycle by Cycle measurement
 Syntax :CBCycle:FILTer[:LINE][:ALL] {OFF|
       <frequency>}
       OFF = Line filter OFF
       <frequency> = 500 Hz, 5.5 kHz, 50 kHz (line filter
       ON, cutoff frequency)
 Example :CBCYCLE:FILTER:LINE:ALL 50KHZ
 Description Does not set line filters for motor input.
 :CBCycle:FILTer[:LINE]:ELEMent<x>
 Function Sets the line filter of individual elements for Cycle
       by Cycle measurement or queries the current
       setting
 Syntax :CBCycle:FILTer[:LINE]:
       ELEMent<x> {OFF|<frequency>}
       :CBCycle:FILTer[:LINE]:ELEMent<x>?
       <x> = 1 to 4 (element)
       OFF = Line filter OFF
       <frequency> = 500 Hz, 5.5 kHz, 50 kHz (line filter
       ON, cutoff frequency)
 Example :CBCYCLE:FILTER:LINE:ELEMENT1 50KHZ
       :CBCYCLE:FILTER:LINE:ELEMENT1? ->
       :CBCYCLE:FILTER:LINE:
       ELEMENT1 50.0E+03
```
### Right column
```text
 :CBCycle:FILTer[:LINE]:MOTor
 Function Sets the motor input line filters for Cycle by Cycle
       measurement or queries the current setting
 Syntax :CBCycle:FILTer[:LINE]:MOTor {OFF|
       <frequency>}
       :CBCycle:FILTer[:LINE]:MOTor?
       OFF = Line filter OFF
       <frequency> = 100 Hz, 50 kHz (line filter ON,
       cutoff frequency)
 Description Available only on models with the motor
       evaluation function (/MTR option).
 :CBCycle:RESet
 Function Resets Cycle by Cycle measurement.
 Syntax :CBCycle:RESet
 Example :CBCYCLE:RESET

 :CBCycle:STARt
 Function Starts Cycle by Cycle measurement.
 Syntax :CBCycle:STARt
 Example :CBCYCLE:START
 :CBCycle:STATe?
 Function Queries the Cycle by Cycle measurement status.
 Syntax :CBCycle:STATe?
 Example :CBCYCLE:STATE? -> RESET
 Description The contents of the response are as follows:
        RESet = Reset status
        STARt = Measuring
        COMPlete = Measurement finished and
        measured results displayed
        TIMEout = Timeout
        ERRFreq = Measurement finished (frequency
        measurement error occurred)
 :CBCycle:SYNChronize?
 Function Queries all settings related to the synchronization
       source for Cycle by Cycle measurement.
 Syntax :CBCycle:SYNChronize?
 Example :CBCYCLE:SYNCHRONIZE? ->
       :CBCYCLE:SYNCHRONIZE:SOURCE U1;
       SLOPE RISE

 :CBCycle:SYNChronize:SLOPe
 Function Sets the slope of the synchronization source
       of Cycle by Cycle measurement or queries the
       current setting.
 Syntax :CBCycle:SYNChronize:SLOPe {RISE|
       FALL}
       :CBCycle:SYNChronize:SLOPe?
 Example :CBCYCLE:SYNCHRONIZE:SLOPE RISE
       :CBCYCLE:SYNCHRONIZE:SLOPE? ->
       :CBCYCLE:SYNCHRONIZE:SLOPE RISE
```

## Page 6-23

### Left column
```text
   :CBCycle:SYNChronize:SOURce
   Function Sets the synchronization source for Cycle by
         Cycle measurement or queries the current
         setting.
   Syntax :CBCycle:SYNChronize:SOURce {U<x>|
         I<x>|EXTernal}
         :CBCycle:SYNChronize:SOURce?
         <x> = 1 to 4 (element)
         EXTernal = External clock input (Ext Clk)
   Example :CBCYCLE:SYNCHRONIZE:SOURCE U1
         :CBCYCLE:SYNCHRONIZE:SOURCE? ->
         :CBCYCLE:SYNCHRONIZE:SOURCE U1
   :CBCycle:TIMEout
   Function Sets the timeout value for Cycle by Cycle
         measurement or queries the current setting.
   Syntax :CBCycle:TIMEout {<NRf>}
         :CBCycle:TIMEout?
         <NRf> = 0 to 3600 (seconds)
         (0 = No timeout)
   Example :CBCYCLE:TIMEOUT 10
         :CBCYCLE:TIMEOUT? ->
         :CBCYCLE:TIMEOUT 10
   :CBCycle:TRIGger?
   Function Queries all settings related to triggers or queries
         the current setting.
   Syntax :CBCycle:TRIGger?
   Example :CBCYCLE:TRIGGER? ->
         :CBCYCLE:TRIGGER:MODE AUTO;
         SOURCE U1;SLOPE RISE;LEVEL 0.0
   Description This is the same query as with the
         “:DISPlay:WAVE:TRIGger?” command.
   :CBCycle:TRIGger:LEVel
   Function Sets the trigger level or queries the current
         setting.
   Syntax :CBCycle:TRIGger:LEVel {<NRf>}
         :CBCycle:TRIGger:LEVel?
         <NRf> = -100.0 to 100.0(%)
   Example :CBCYCLE:TRIGGER:LEVEL 0
         :CBCYCLE:TRIGGER:LEVEL? ->
         :CBCYCLE:TRIGGER:LEVEL 0.0
   Description This is the same setting or query as with
         the “:DISPlay:WAVE:TRIGger:LEVel?”
         command.
   :CBCycle:TRIGger:MODE
   Function Sets the trigger mode or queries the current
         setting.
   Syntax :CBCycle:TRIGger:MODE {AUTO|NORMal}
         :CBCycle:TRIGger:MODE?
   Example :CBCYCLE:TRIGGER:MODE AUTO
         :CBCYCLE:TRIGGER:MODE? ->
         :CBCYCLE:TRIGGER:MODE AUTO
   Description This is the same setting or query as with the
         “:DISPlay:WAVE:TRIGger:MODE” command.
```
### Right column
```text
                    6.4 CBCycle Group

 :CBCycle:TRIGger:SLOPe
 Function Sets the trigger slope or queries the current
       setting.
 Syntax :CBCycle:TRIGger:SLOPe {RISE|FALL|
       BOTH}
       :CBCycle:TRIGger:SLOPe?
 Example :CBCYCLE:TRIGGER:SLOPE RISE
       :CBCYCLE:TRIGGER:SLOPE? ->
       :CBCYCLE:TRIGGER:SLOPE RISE
 Description This is the same setting or query as with the
       “:DISPlay:WAVE:TRIGger:SLOPe” command.
 :CBCycle:TRIGger:SOURce
 Function Sets the trigger source or queries the current
       setting.
 Syntax :CBCycle:TRIGger:SOURce {U<x>|I<x>|
       EXTernal}
       :CBCycle:TRIGger:SOURce?
       <x> = 1 to 4 (element)
       EXTernal = External trigger input (Ext Clk)
 Example :CBCYCLE:TRIGGER:SOURCE U1
       :CBCYCLE:TRIGGER:SOURCE? ->
       :CBCYCLE:TRIGGER:SOURCE U1
 Description This is the same setting or query as with
       the “:DISPlay:WAVE:TRIGger:SOURce”
       command.
```

## Page 6-24

### Section introduction
```text
   6.5    COMMunicate      Group

 The commands in this group deal with communications. There are no front panel keys that correspond to the
 commands in this group.
```
### Left column
```text
 :COMMunicate?
 Function Queries all settings related to communications.
 Syntax :COMMunicate?
 Example :COMMUNICATE? ->
       :COMMUNICATE:HEADER 1;OPSE 96;
       OVERLAP 96;VERBOSE 1

 :COMMunicate:HEADer
 Function Sets whether to add a header to the response to
       a query (example DISPLAY:MODE NUMERIC) or
       not add the header (example NUMERIC).
 Syntax :COMMunicate:HEADer {<Boolean>}
       :COMMunicate:HEADer?
 Example :COMMUNICATE:HEADER ON
       :COMMUNICATE:HEADER? ->
       :COMMUNICATE:HEADER 1
 :COMMunicate:LOCKout
 Function Sets or clears local lockout.
 Syntax :COMMunicate:LOCKout {<Boolean>}
       :COMMunicate:LOCKout?
 Example :COMMUNICATE:LOCKOUT ON
       :COMMUNICATE:LOCKOUT? ->
       :COMMUNICATE:LOCKOUT 1
 Description This command is dedicated to the optional RS-
       232, USB, or Ethernet interface. An interface
       message is available for the GP-IB interface.
 :COMMunicate:OPSE(Operation Pending
 Status Enable register)
 Function Sets the overlap command that is used by the
       *OPC, *OPC?, and *WAI commands or queries
       the current setting.
 Syntax :COMMunicate:OPSE <Register>
       :COMMunicate:OPSE?
       <Register> = 0 to 65535, see the command
       diagram for :COMMunicate:WAIT? on page
       6-25.
 Example :COMMUNICATE:OPSE 65535
       :COMMUNICATE:OPSE? ->
       :COMMUNICATE:OPSE 96
 Description In the above example, all bits are set to 1 to make
       all overlap commands applicable. However, bits
       fixed to 0 are not set to 1. Thus, the response to
       the query indicates 1 for bits 5 and 6 only.
```
### Right column
```text
 :COMMunicate:OPSR?(Operation Pending
 Status Register)
 Function Queries the value of the operation pending status
       register.
 Syntax :COMMunicate:OPSR?
 Example :COMMUNICATE:OPSR? -> 0
 Description For details on the operation pending
       status register, see the figure for the
       :COMMunicate:WAIT? command (page 6-25).
 :COMMunicate:OVERlap
 Function Sets the commands that will operate as overlap
       commands or queries the current setting.
 Syntax :COMMunicate:OVERlap <Register>
       :COMMunicate:OVERlap?
       <Register> = 0 to 65535, see the command
       diagram for :COMMunicate:WAIT? on page
       6-25.
 Example :COMMUNICATE:OVERLAP 65535
       :COMMUNICATE:OVERLAP? ->
       :COMMUNICATE:OVERLAP 96
 Description • In the above example, all bits are set to 1
        to make all overlap commands applicable.
        However, bits fixed to 0 are not set to 1. Thus,
        the response to the query indicates 1 for bits 5
        and 6 only.
       • For the description regarding how
        to synchronize the program using
        COMMunicate:OVERlap, see page 5-8.
       • In the above example, bits 5 and 6 are set to
        1 to make all overlap commands applicable
        (see the figure for the :COMMunicate:WAIT?
        command (page 6-25)).
 :COMMunicate:REMote
 Function Sets remote or local. ON is remote mode.
 Syntax :COMMunicate:REMote {<Boolean>}
       :COMMunicate:REMote?
 Example :COMMUNICATE:REMOTE ON
       :COMMUNICATE:REMOTE? ->
       :COMMUNICATE:REMOTE 1
 Description This command is dedicated to the optional RS-
       232, USB, or Ethernet interface. An interface
       message is available for the GP-IB interface.
```

## Page 6-25

### Left column
```text
   :COMMunicate:STATus?
   Function Queries line-specific status.
   Syntax :COMMunicate:STATus?
   Example :COMMUNICATE:STATUS? ->
         :COMMUNICATE:STATUS 0
   Description The meaning of each status bit is as follows:
          Bit   GP-IB     RS-232
          0     Unrecoverable Parity error
                transmission error
          1     Always 0  Framing error
          2     Always 0  Break character
                          detected
          3 or greater Always 0 Always 0
         The value 0 is always returned for the optional
         USB or Ethernet interface.
         The status bit is set when the corresponding
         cause occurs and cleared when it is read.
   :COMMunicate:VERBose
   Function Sets whether to return the response
         to a query using full spelling (example
         :INPUT:VOLTAGE:RANGE:ELEMENT1
         1.000E+03) or using abbreviation (example
         :VOLT:RANG:ELEM 1.000E+03).
   Syntax :COMMunicate:VERBose {<Boolean>}
         :COMMunicate:VERBose?
   Example :COMMUNICATE:VERBOSE ON
         :COMMUNICATE:VERBOSE? ->
         :COMMUNICATE:VERBOSE 1
   :COMMunicate:WAIT
   Function Waits for one of the specified extended events to
         occur.
   Syntax :COMMunicate:WAIT <Register>
         <Register> = 0 to 65535 (extended event register,
         see page 7-7.)
   Example :COMMUNICATE:WAIT 1
   Description For the description regarding how to synchronize
         the program using COMMunicate:WAIT, see
         page 5-10.
   :COMMunicate:WAIT?
   Function Creates the response that is returned when the
         specified event occurs.
   Syntax :COMMunicate:WAIT? <Register>
         <Register> = 0 to 65535 (extended event register,
         see page 7-7.)
   Example :COMMUNICATE:WAIT? 65535 -> 1
         Operation pending status register/Overlap enable
         register
         15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0
         0 0 0 0 0 0 0 0 0 ACSPRN 0 0 0 0 0
         When bit 5 (PRN) = 1:
         Built-in printer operation not complete
         When bit 6 (ACS) = 1:
          Access to the medium not complete.
```
### Right column
```text
                 6.5 COMMunicate Group
```

## Page 6-26

### Section introduction
```text
   6.6    CURSor    Group

 The commands in this group deal with cursor measurements. You can make the same settings and inquiries as when
 CURSOR (SHIFT+MEASURE) on the front panel is used.
```
### Left column
```text
 :CURSor?
 Function Queries all settings related to the cursor
       measurement.
 Syntax :CURSor?
 Example :CURSOR? -> :CURSOR:WAVE:STATE 0;
       TRACE1 U1;TRACE2 I1;PATH MAX;
       POSITION1 10.0E-03;
       POSITION2 40.0E-03;:CURSOR:BAR:
       STATE 0;POSITION1 1;POSITION2 15;:
       CURSOR:TREND:STATE 0;TRACE1 1;
       TRACE2 2;POSITION1 100;
       POSITION2 900
 :CURSor:BAR?
 Function Queries all settings related to the cursor
       measurement of the bar graph display.
 Syntax :CURSor:BAR?
 Example :CURSOR:BAR? -> :CURSOR:BAR:
       STATE 1;POSITION1 1;POSITION2 15
 Description This command is valid only on models with the
       advanced computation function (/G6 option).

 :CURSor:BAR:POSition<x>
 Function Sets the cursor position (order) on the bar graph
       display or queries the current setting.
 Syntax :CURSor:BAR:POSition<x> {<NRf>}
       :CURSor:BAR:POSition<x>?
       <x> = 1, 2 (1 = C1 +, 2 = C2 x)
       <NRf> = 0 to 100
 Example :CURSOR:BAR:POSITION1 1
       :CURSOR:BAR:POSITION1? ->
       :CURSOR:BAR:POSITION1 1
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :CURSor:BAR[:STATe]
 Function Turns ON/OFF the cursor display on the bar
       graph display or queries the current setting.
 Syntax :CURSor:BAR[:STATe] {<Boolean>}
       :CURSor:BAR:STATe?
 Example :CURSOR:BAR:STATE ON
       :CURSOR:BAR:STATE? ->
       :CURSOR:BAR:STATE 1
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
```
### Right column
```text
 :CURSor:BAR:{Y<x>|DY}?
 Function Queries the cursor measurement value on the
       bar graph display.
 Syntax :CURSor:BAR:{Y<x>|DY}?
       Y<x> = Y-axis value at the cursor position (Y1 =
       Y1+, Y2+, Y3+ Y2 = Y1x, Y2x, Y3x)
       DY = Y-axis value between cursors (∆Y1, ∆Y2,
       and ∆Y3)
       <x> = 1, 2 (1 = C1 +, 2 = C2 x)
 Example :CURSOR:BAR:Y1? -> 78.628E+00
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • When multiple bar graphs are displayed, the
        cursor measurement values of each bar graph
        are returned in order.
       • If the cursor display is not turned ON on the
        bar graph, “NAN (Not A Number)” is returned.
 :CURSor:FFT?
 Function Queries all settings related to the cursor
       measurement on the FFT waveform display.
 Syntax :CURSor:FFT?
 Example :CURSOR:FFT? -> :CURSOR:FFT:
       STATE 0;TRACE1 FFT1;TRACE2 FFT2;
       POSITION1 100;POSITION2 900
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :CURSor:FFT:POSition<x>
 Function Sets the cursor position on the FFT waveform
       display or queries the current setting.
 Syntax :CURSor:FFT:POSition<x> {<NRf>}
       :CURSor:FFT:POSition<x>?
       <x> = 1, 2(1 = C1 +, 2 = C2 x)
       <NRf> = 0 to 1001
 Example :CURSOR:FFT:POSITION1 20
       :CURSOR:FFT:POSITION1? ->
       :CURSOR:FFT:POSITION1 20
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
```

## Page 6-27

### Left column
```text
   :CURSor:FFT[:STATe]
   Function Turns ON/OFF the cursor display on the FFT
         waveform display or queries the current setting.
   Syntax :CURSor:FFT[:STATe] {<Boolean>}
         :CURSor:FFT:STATe?
   Example :CURSOR:FFT:STATE OFF
         :CURSOR:FFT:STATE? ->
         :CURSOR:FFT:STATE 0
   Description This command is valid only on models with the
         advanced computation function (/G6 option).
   :CURSor:FFT:TRACe<x>
   Function Sets the cursor target on the FFT waveform
         display or queries the current setting.
   Syntax :CURSor:FFT:TRACe<x> {FFT<x>}
         :CURSor:FFT:TRACe<x>?
         <x> of TRACe<x> = 1 or 2 (1 = C1 +, 2 = C2 x)
         <x> of FFT<x> = 1 or 2 (FFT)
   Example :CURSOR:FFT:TRACE1 FFT1
         :CURSOR:FFT:TRACE1? ->
         :CURSOR:FFT:TRACE1 FFT1
   Description This command is valid only on models with the
         advanced computation function (/G6 option).
   :CURSor:FFT:{X<x>|DX|Y<x>|DY}?
   Function Queries the cursor measurement value on the
         FFT waveform display.
   Syntax :CURSor:FFT:{X<x>|DX|Y<x>|DY}?
         X<x> = X-axis value of the cursor position (X1 =
         X+, X2 = Xx)
         DX = X-axis value between cursors (∆X)
         Y<x> = Y-axis value of the cursor position (Y1 =
         Y+, Y2 = Yx)
         DY = Y-axis value between cursors (∆Y)
         <x> = 1, 2(1 = C1 +, 2 = C2 x)
   Example :CURSOR:FFT:Y1? -> 78.628E+00
   Description • This command is valid only on models with the
          advanced computation function (/G6 option).
         • If the cursor display is not turned ON in the
          FFT waveform display, “NAN (Not A Number)”
          is returned.
   :CURSor:TRENd?
   Function Queries all settings related to the cursor
         measurement of the trend display.
   Syntax :CURSor:TRENd?
   Example :CURSOR:TREND? -> :CURSOR:TREND:
         STATE 1;TRACE1 1;TRACE2 2;
         POSITION1 100;POSITION2 900
```
### Right column
```text
                    6.6 CURSor Group

 :CURSor:TRENd:POSition<x>
 Function Sets the cursor position on the trend display or
       queries the current setting.
 Syntax :CURSor:TRENd:POSition<x> {<NRf>}
       :CURSor:TRENd:POSition<x>?
       <x> = 1, 2 (1 = C1 +, 2 = C2 x)
       <NRf> = 0 to 1001
 Example :CURSOR:TREND:POSITION1 10
       :CURSOR:TREND:POSITION1? ->
       :CURSOR:TREND:POSITION1 10
 :CURSor:TRENd[:STATe]
 Function Turns ON/OFF the cursor display on the trend
       display or queries the current setting.
 Syntax :CURSor:TRENd[:STATe] {<Boolean>}
       :CURSor:TRENd:STATe?
 Example :CURSOR:TREND:STATE ON
       :CURSOR:TREND:STATE? ->
       :CURSOR:TREND:STATE 1

 :CURSor:TRENd:TRACe<x>
 Function Sets the cursor target on the trend display or
       queries the current setting.
 Syntax :CURSor:TRENd:TRACe<x> {<NRf>}
       :CURSor:TRENd:TRACe<x>?
       <x> = 1, 2 (1 = C1 +, 2 = C2 x)
       <NRf> = 1 to 16 (T1 to T16)
 Example :CURSOR:TREND:TRACE1 1
       :CURSOR:TREND:TRACE1? ->
       :CURSOR:TREND:TRACE1 1
 :CURSor:TRENd:{X<x>|Y<x>|DY}?
 Function Queries the cursor measurement value on the
       trend display.
 Syntax :CURSor:TRENd:{X<x>|Y<x>|DY}?
       X<x> = Trend time string of the cursor position (X1
       = D+, X2 = Dx)
       Y<x> = Y-axis value of the cursor position (Y1 =
       Y+, Y2 = Yx)
       DY = Y-axis value between cursors (∆Y)
       <x> = 1, 2 (1 = C1 +, 2 = C2 x)
 Example :CURSOR:TREND:X1? ->
       “2005/01/01 12:34:56”
       :CURSOR:TREND:Y1? -> 78.628E+00
 Description If the cursor display is not turned ON on the
       trend, the following results.
       For X<x>: “****/**/** **:**:**” is returned.
       For Y<x> and DY: “NAN (Not A Number)” is
       returned.
```

## Page 6-28

### Left column
```text
 6.6 CURSor Group

 :CURSor:WAVE?
 Function Queries all settings related to the cursor
       measurement on the waveform display.
 Syntax :CURSor:WAVE?
 Example :CURSOR:WAVE? -> :CURSOR:WAVE:
       STATE 1;TRACE1 U1;TRACE2 I1;
       PATH MAX;POSITION1 10.0E-03;
       POSITION2 40.0E-03
 :CURSor:WAVE:PATH
 Function Sets the cursor path on the waveform display or
       queries the current setting.
 Syntax :CURSor:WAVE:PATH {MAX|MIN|MID}
       :CURSor:WAVE:PATH?
 Example :CURSOR:WAVE:PATH MAX
       :CURSOR:WAVE:PATH? ->
       :CURSOR:WAVE:PATH MAX

 :CURSor:WAVE:POSition<x>
 Function Sets the cursor position on the waveform display
       or queries the current setting.
 Syntax :CURSor:WAVE:POSition<x> {<Time>}
       :CURSor:WAVE:POSition<x>?
       <x> = 1, 2 (1 = C1 +, 2 = C2 x)
       <Time> = 0 to 20.00 s
 Example :CURSOR:WAVE:POSITION1 10MS
       :CURSOR:WAVE:POSITION1? ->
       :CURSOR:WAVE:POSITION1 10.0E-03
 Description The selectable range and resolution of <Time> is
       determined by the Time/div value of the waveform
       (:DISPlay:WAVE:TDIV).
 :CURSor:WAVE[:STATe]
 Function Turns ON/OFF the cursor display on the
       waveform display or queries the current setting.
 Syntax :CURSor:WAVE[:STATe] {<Boolean>}
       :CURSor:WAVE:STATe?
 Example :CURSOR:WAVE:STATE ON
       :CURSOR:WAVE:STATE? ->
       :CURSOR:WAVE:STATE 1
```
### Right column
```text
 :CURSor:WAVE:TRACe<x>
 Function Sets the cursor target on the waveform display or
       queries the current setting.
 Syntax :CURSor:WAVE:TRACe<x> {U<x>|I<x>|
       SPEed|TORQue|MATH<x>}
       :CURSor:WAVE:TRACe<x>?
       <x> of TRACe<x> = 1 or 2 (1 = C1 +, 2 = C2 x)
       <x> of U<x>, I<x> = 1 to 4
       <x> of MATH<x> = 1 to 2 (MATH)
 Example :CURSOR:WAVE:TRACE1 U1
       :CURSOR:WAVE:TRACE1? ->
       :CURSOR:WAVE:TRACE1 U1
 Description • {SPEed|TORQue} are valid only on models
        with the motor evaluation function (/MTR
        option).
       • MATH<x> is valid only on models with the
        advanced computation function (/G6 option).
 :CURSor:WAVE:{X<x>|DX|PERDt|Y<x>|
 DY}?
 Function Queries the cursor measurement value on the
       waveform display.
 Syntax :CURSor:WAVE:{X<x>|DX|PERDt|Y<x>|
       DY}?
       X<x> = X-axis value of the cursor position (X1 =
       X+, X2 = Xx)
       DX = X-axis value between cursors (∆X)
       PERDt = 1/DT (1/∆X) value between cursors
       Y<x> = Y-axis value of the cursor position (Y1 =
       Y+, Y2 = Yx)
       DY = Y-axis value between cursors (∆Y)
       <x> = 1, 2 (1 = C1 +, 2 = C2 x)
 Example :CURSOR:WAVE:Y1? -> 78.628E+00
 Description If the cursor display is not turned ON in the
       waveform display, “NAN (Not A Number)” is
       returned.
```

## Page 6-29

### Section introduction
```text
     6.7    DISPlay   Group

   The commands in this group deal with the screen display.
   You can make the same settings and inquiries as when the keys in the DISPLAY area and the ITEM & ELEMENT
   area on the front panel are used.
```
### Left column
```text
   :DISPlay?
   Function Queries all settings related to the screen display.
   Syntax :DISPlay?
   Example • Example when the display mode
          (:DISPlay:MODE) is “NUMeric (numeric
          display)”
          :DISPLAY? -> :DISPLAY:MODE NUMERIC;
          (Response to “:DISPlay:NUMeric?”
          with the first “:DISPLAY:” section
          removed);:DISPLAY:INFORMATION:
          STATE 0;
          PAGE 1
         • Example when the display mode
          (:DISPlay:MODE) is “WAVE (waveform
          display)”
          :DISPLAY? -> :DISPLAY:MODE
          WAVE; (Response to “:DISPlay:WAVE?”
          with the first “:DISPLAY:” section
          removed);:DISPLAY:INFORMATION:
          STATE 0;
          PAGE 1
         • Example when the display mode
          (:DISPlay:MODE) is “NWAVe”
          :DISPLAY? -> :DISPLAY:MODE NWAVE;
          (Response to “:DISPlay:NUMeric?”
          with the first “:DISPLAY:” section
          removed);(same as the response to
          “:DISPlay:WAVE?”);:DISPLAY:
          INFORMATION:STATE 0;PAGE 1
   Description Returns all settings corresponding to the display
         mode (:DISPlay:MODE).
   :DISPlay:BAR?
   Function Queries all settings related to the bar graph.
   Syntax :DISPlay:BAR?
   Example :DISPLAY:BAR? -> :DISPLAY:BAR:
         FORMAT SINGLE;ITEM1 U,1;ITEM2 I,1;
         ITEM3 P,1;ORDER 1,100
   Description This command is valid only on models with the
         advanced computation function (/G6 option).
```
### Right column
```text
 :DISPlay:BAR:FORMat
 Function Sets the display format of the bar graph or
       queries the current setting.
 Syntax :DISPlay:BAR:FORMat {SINGle|DUAL|
       TRIad}
       :DISPlay:BAR:FORMat?
 Example :DISPLAY:BAR:FORMAT SINGLE
       :DISPLAY:BAR:FORMAT? ->
       :DISPLAY:BAR:FORMAT SINGLE
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :DISPlay:BAR:ITEM<x>
 Function Sets the bar graph item (function and element) or
       queries the current setting.
 Syntax :DISPlay:BAR:ITEM<x> {<Function>,
       <Element>}
       :DISPlay:BAR:ITEM<x>?
       <x> = 1 to 3 (item number)
       <Function> = {U|I|P|S|Q|LAMBda|...} (See
       the function selection list (2) on page 6-46.)
       <Element> = 1 to 4
 Example :DISPLAY:BAR:ITEM1 U,1
       :DISPLAY:BAR:ITEM1? ->
       :DISPLAY:BAR:ITEM1 U,1
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
```

## Page 6-30

### Left column
```text
 6.7 DISPlay Group

 :DISPlay:BAR:ORDer
 Function Sets the start and end orders of the bar graph or
       queries the current setting.
 Syntax :DISPlay:BAR:ORDer {<NRf>,<NRf>}
       :DISPlay:BAR:ORDer?
       1st <NRf> = 0 to 90 (start order to be displayed)
       2nd <NRf> = 10 to 100 (end order to be
       displayed)
 Example :DISPLAY:BAR:ORDER 1,100
       :DISPLAY:BAR:ORDER? ->
       :DISPLAY:BAR:ORDER 1,100
 Description • This command is valid only on models with the
        advanced computation function (/G6 option) .
       • Set the start order and then the end order.
       • Set the end order so that it is greater than or
        equal to (start order + 10).
 :DISPlay:CBCycle?
 Function Queries all settings related to the Cycle by Cycle
       display.
 Syntax :DISPlay:CBCycle?
 Example :DISPLAY:CBCYCLE? -> :DISPLAY:
       CBCYCLE:ITEM1 FREQ;ITEM2 U,1;
       ITEM3 I,1;ITEM4 P,1;ITEM5 S,1;
       CURSOR 1
 :DISPlay:CBCycle:CURSor
 Function Sets the cursor position of the Cycle by Cycle
       display or queries the current setting.
 Syntax :DISPlay:CBCycle:CURSor {<NRf>}
       :DISPlay:CBCycle:CURSor?
       <NRf> = 1 to 3000 (cursor position)
 Example :DISPLAY:CBCYCLE:CURSOR 1
       :DISPLAY:CBCYCLE:CURSOR? ->
       :DISPLAY:CBCYCLE:CURSOR 1
 Description Specifies the cursor position by the cycle number.
```
### Right column
```text
 :DISPlay:CBCycle:ITEM<x>
 Function Sets the displayed items (function and element)
       of the Cycle by Cycle display or queries the
       current setting.
 Syntax :DISPlay:CBCycle:
       ITEM<x> {<Function>,<Element>}
       :DISPlay:CBCycle:ITEM<x>?
       <x> = 1 to 5 (item number)
       <Function> = {FREQ|U|I|P|S|Q|LAMBda|
       SPEed|TORQue|PM}
       <Element> = {<NRf>|SIGMa|SIGMB} (<NRf>
       = 1 to 4)
 Example :DISPLAY:CBCYCLE:ITEM1 U,1
       :DISPLAY:CBCYCLE:ITEM1? ->
       :DISPLAY:CBCYCLE:ITEM1 U,1
 Description • When <Function> = {FREQ|SPEed|
        TORQue|PM}, <Element> need not be
        specified. <Element> is omitted from the
        response.
       • When <Element> is omitted, Element 1 is set.
       • {SPEed|TORQue|PM} is only available on
        models with the motor evaluation function (/
        MTR option).
 :DISPlay:CBCycle:PAGE
 Function Sets the number of the displayed page of the
       Cycle by Cycle display or queries the current
       setting.
 Syntax :DISPlay:CBCycle:PAGE {<NRf>}
       :DISPlay:CBCycle:PAGE?
       <NRf> = 1 to 150 (page number)
 Example :DISPLAY:CBCYCLE:PAGE 1
       :DISPLAY:CBCYCLE:PAGE? ->
       :DISPLAY:CBCYCLE:PAGE 1
 Description When a page number is set, the cursor moves to
       the top of the specified page.
 :DISPlay:FFT?
 Function Queries all settings related to the FFT waveform
       display.
 Syntax :DISPlay:FFT?
 Example :DISPLAY:FFT? -> :DISPLAY:FFT:
       FORMAT SINGLE;POINT 20000;
       WINDOW RECTANGLE;SCOPE 0,10000;
       VSCALE LOG;SPECTRUM LINE;FFT1:
       STATE 1;OBJECT U1;LABEL “FFT1”;:
       DISPLAY:FFT:FFT2:STATE 1;OBJECT I1;
       LABEL “FFT2”
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
```

## Page 6-31

### Left column
```text
   :DISPlay:FFT:FFT<x>?
   Function Queries all settings related to the FFT waveform.
   Syntax :DISPlay:FFT:FFT<x>?
         <x> = 1, 2 (FFT)
   Example :DISPLAY:FFT:FFT1? -> :DISPLAY:FFT:
         FFT1:STATE 1;OBJECT U1;LABEL “FFT1”
   Description This command is valid only on models with the
         advanced computation function (/G6 option).
   :DISPlay:FFT:FFT<x>:LABel
   Function Sets the label of the FFT waveform or queries the
         current setting.
   Syntax :DISPlay:FFT:FFT<x>:
         LABel {<String>}
         :DISPlay:FFT:FFT<x>:LABel?
         <x> = 1, 2 (FFT)
         <String> = Up to 8 characters
   Example :DISPLAY:FFT:FFT1:LABEL “FFT1”
         :DISPLAY:FFT:FFT1:LABEL? ->
         :DISPLAY:FFT:FFT1:LABEL “FFT1”
   Description This command is valid only on models with the
         advanced computation function (/G6 option).
   :DISPlay:FFT:FFT<x>:OBJect
   Function Sets the source waveform of the FFT computation
         or queries the current setting.
   Syntax :DISPlay:FFT:FFT<x>:OBJect {U<x>|
         I<x>|P<x>|PA|PB|Q<x>|QA|QB|SPEed|
         TORQue}
         :DISPlay:FFT:FFT<x>:OBJect?
         <x> of FFT<x> = 1, 2 (FFT)
         <x> of U<x>, I<x>, P<x>, Q<x> = 1 to 4 (element)
         PA, QA = PΣA, QΣA (only on models with 2 to 4
         elements)
         PB, QB = PΣB, QΣB (only on models with 4
         elements)
   Example :DISPLAY:FFT:FFT1:OBJECT U1
         :DISPLAY:FFT:FFT1:OBJECT? ->
         :DISPLAY:FFT:FFT1:OBJECT U1
   Description • This command is valid only on models with the
          advanced computation function (/G6 option).
         • {SPEed|TORQue} are valid only on models
          with the motor evaluation function (/MTR
          option).
```
### Right column
```text
                    6.7 DISPlay Group

 :DISPlay:FFT:FFT<x>[:STATe]
 Function Turns ON/OFF the FFT waveform display or
       queries the current setting.
 Syntax :DISPlay:FFT:
       FFT<x>[:STATe] {<Boolean>}
       :DISPlay:FFT:FFT<x>:STATe?
       <x> = 1, 2 (FFT)
 Example :DISPLAY:FFT:FFT1:STATE ON
       :DISPLAY:FFT:FFT1:STATE? ->
       :DISPLAY:FFT:FFT1:STATE 1
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :DISPlay:FFT:FORMat
 Function Sets the display format of the FFT waveform or
       queries the current setting.
 Syntax :DISPlay:FFT:FORMat {SINGle|DUAL}
       :DISPlay:FFT:FORMat?
 Example :DISPLAY:FFT:FORMAT SINGLE
       :DISPLAY:FFT:FORMAT? ->
       :DISPLAY:FFT:FORMAT SINGLE
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :DISPlay:FFT:POINt
 Function Sets the number of points of the FFT computation
       or queries the current setting.
 Syntax :DISPlay:FFT:POINt {<NRf>}
       :DISPlay:FFT:POINt?
       <NRf> = 20000, 200000
 Example :DISPLAY:FFT:POINT 20000
       :DISPLAY:FFT:POINT? ->
       :DISPLAY:FFT:POINT 20000
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :DISPlay:FFT:SCOPe
 Function Sets the display range of the FFT waveform or
       queries the current setting.
 Syntax :DISPlay:FFT:SCOPe {<NRf>,<NRf>}
       :DISPlay:FFT:SCOPe?
       1st <NRf> = 0 to 99990 (display start point)
       2nd <NRf> = 10 to 100000 (display end point)
 Example :DISPLAY:FFT:SCOPE 0,10000
       :DISPLAY:FFT:SCOPE? ->
       :DISPLAY:FFT:SCOPE 0,10000
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • Set the start point and then the end point.
       • Set the end point so that it is greater than or
        equal to (start point + 10).
```

## Page 6-32

### Left column
```text
 6.7 DISPlay Group

 :DISPlay:FFT:SPECtrum
 Function Sets the display spectrum format of the FFT
       waveform or queries the current setting.
 Syntax :DISPlay:FFT:SPECtrum {LINE|BAR}
       :DISPlay:FFT:SPECtrum?
 Example :DISPLAY:FFT:SPECTRUM LINE
       :DISPLAY:FFT:SPECTRUM? ->
       :DISPLAY:FFT:SPECTRUM LINE
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :DISPlay:FFT:VSCale
 Function Sets the display scale of the vertical axis of the
       FFT waveform or queries the current setting.
 Syntax :DISPlay:FFT:VSCale {LINear|LOG}
       :DISPlay:FFT:VSCale?
 Example :DISPLAY:FFT:VSCALE LOG
       :DISPLAY:FFT:VSCALE? ->
       :DISPLAY:FFT:VSCALE LOG
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :DISPlay:FFT:WINDow
 Function Sets the window function of the FFT computation
       or queries the current setting.
 Syntax :DISPlay:FFT:WINDow {RECTangle|
       HANNing|FLATtop}
       :DISPlay:FFT:WINDow?
 Example :DISPLAY:FFT:WINDOW RECTANGLE
       :DISPLAY:FFT:WINDOW? ->
       :DISPLAY:FFT:WINDOW RECTANGLE
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :DISPlay:FLICker?
 Function Queries all settings related to flicker measurement
       display.
 Syntax :DISPlay:FLICker?
 Example :DISPLAY:FLICKER? ->
       :DISPLAY:FLICKER:ELEMENT 1;PERIOD 1
 Description Only available with the flicker measurement
       function (/FL option).

 :DISPlay:FLICker:ELEMent
 Function Sets the element to be displayed for flicker
       measurement display or queries the current
       setting.
 Syntax :DISPlay:FLICker:ELEMent {<NRf>}
       :DISPlay:FLICker:ELEMent?
       <NRf> = 1 to 4 (element)
 Example :DISPLAY:FLICKER:ELEMENT 1
       :DISPLAY:FLICKER:ELEMENT? ->
       :DISPLAY:FLICKER:ELEMENT 1
 Description Only available with the flicker measurement
       function (/FL option).
```
### Right column
```text
 :DISPlay:FLICker:PAGE
 Function Sets the page numbers to be displayed for flicker
       measurement display or queries the current
       setting.
 Syntax :DISPlay:FLICker:PAGE {<NRf>}
       :DISPlay:FLICker:PAGE?
       <NRf> = 1 to 9 (page number)
 Example :DISPLAY:FLICKER:PAGE 1
       :DISPLAY:FLICKER:PAGE? ->
       :DISPLAY:FLICKER:PAGE 1
 Description Only available with the flicker measurement
       function (/FL option).
 :DISPlay:FLICker:PERiod
 Function Sets the display observation period number
       for flicker measurement display or queries the
       current setting.
 Syntax :DISPlay:FLICker:PERiod {<NRf>}
       :DISPlay:FLICker:PERiod?
       <NRf> = 1 to 99 (observation period number)
 Example :DISPLAY:FLICKER:PERIOD 1
       :DISPLAY:FLICKER:PERIOD? ->
       :DISPLAY:FLICKER:PERIOD 1
 Description Only available with the flicker measurement
       function (/FL option).
 :DISPlay:INFOrmation?
 Function Queries all settings related to the display of the
       setup parameter list.
 Syntax :DISPlay:INFOrmation?
 Example :DISPLAY:INFORMATION? ->
       :DISPLAY:INFORMATION:STATE 0;PAGE 1

 :DISPlay:INFOrmation:PAGE
 Function Sets the page number of the display of setup
       parameter list or queries the current setting.
 Syntax :DISPlay:INFOrmation {<NRf>}
       :DISPlay:INFOrmation?
       <NRf> = 1 to 4 (page number)
 Example :DISPLAY:INFORMATION:PAGE 1
       :DISPLAY:INFORMATION:PAGE? ->
       :DISPLAY:INFORMATION:PAGE 1
 :DISPlay:INFOrmation[:STATe]
 Function Turns ON/OFF the display of the setup parameter
       list or queries the current setting.
 Syntax :DISPlay:INFOrmation
       [:STATe] {<Boolean>}
       :DISPlay:INFOrmation:STATe?
 Example :DISPLAY:INFORMATION:STATE ON
       :DISPLAY:INFORMATION:STATE? ->
       :DISPLAY:INFORMATION:STATE 1
```

## Page 6-33

### Left column
```text
   :DISPlay:MATH?
   Function Queries all settings related to the computed
         waveform display.
   Syntax :DISPlay:MATH?
   Example :DISPLAY:MATH? -> :DISPLAY:MATH:
         MATH1:EXPRESSION “U1*I1”;SCALING:
         MODE AUTO;CENTER 0.0000E+00;SDIV
         25.000E+00;:DISPLAY:MATH:MATH1:
         UNIT “W”:LABEL “Math1”;:DISPLAY:
         MATH:MATH2:EXPRESSION “ABS(U1)”;
         SCALING:MODE AUTO;
         CENTER 0.0000E+00;SDIV 25.000E+00;:
         DISPLAY:MATH:MATH2:UNIT “V”:
         LABEL “Math2”;:DISPLAY:MATH:
         CONSTANT1 1.0000E+00;
         CONSTANT2 2.0000E+00;
         CONSTANT3 3.0000E+00;
         CONSTANT4 4.0000E+00;
         CONSTANT5 5.0000E+00;
         CONSTANT6 6.0000E+00;
         CONSTANT7 7.0000E+00;
         CONSTANT8 8.0000E+00
   Description This command is valid only on models with the
         advanced computation function (/G6 option).
   :DISPlay:MATH:CONStant<x>
   Function Sets the constant to be used in the waveform
         computing equation or queries the current setting.
   Syntax :DISPlay:MATH:CONStant<x> {<NRf>}
         :DISPlay:MATH:CONStant<x>?
         <x> = 1 to 8 (K1 to K8)
         <NRf> = –9.9999E+30 to 9.9999E+30
   Example :DISPLAY:MATH:CONSTANT1 1.0000E+00
         :DISPLAY:MATH:CONSTANT1? ->
         :DISPLAY:MATH:CONSTANT1 1.0000E+00
   Description This command is valid only on models with the
         advanced computation function (/G6 option).
   :DISPlay:MATH:MATH<x>?
   Function Queries all settings related to the computed
         waveform.
   Syntax :DISPlay:MATH:MATH<x>?
         <x> = 1, 2 (MATH)
   Example :DISPLAY:MATH:MATH1? -> :DISPLAY:
         MATH:MATH1:EXPRESSION “U1*I1”;
         SCALING:MODE AUTO;
         CENTER 0.0000E+00;SDIV 25.000E+00;:
         DISPLAY:MATH:MATH1:UNIT “W”:
         LABEL “Math1”
   Description This command is valid only on models with the
         advanced computation function (/G6 option).
```
### Right column
```text
                    6.7 DISPlay Group

 :DISPlay:MATH:MATH<x>:EXPRession
 Function Sets the equation of the waveform computation
       or queries the current setting.
 Syntax :DISPlay:MATH:MATH<x>:
       EXPRession {<String>}
       :DISPlay:MATH:MATH<x>:EXPRession?
       <x> = 1, 2 (MATH)
       <String> = Up to 50 characters
 Example :DISPLAY:MATH:MATH1:
       EXPRESSION “U1*I1”
       :DISPLAY:MATH:MATH1:EXPRESSION? ->
       :DISPLAY:MATH:MATH1:
       EXPRESSION “U1*I1”
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :DISPlay:MATH:MATH<x>:LABel
 Function Sets the label of the computed waveform or
       queries the current setting.
 Syntax :DISPlay:MATH:MATH<x>:
       LABel {<String>}
       :DISPlay:MATH:MATH<x>:LABel?
       <x> = 1, 2 (MATH)
       <String> = Up to 8 characters
 Example :DISPLAY:MATH:MATH1:LABEL “Math1”
       :DISPLAY:MATH:MATH1:LABEL? ->
       :DISPLAY:MATH:MATH1:LABEL “Math1”
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :DISPlay:MATH:MATH<x>:SCALing?
 Function Queries all settings related to the scaling of the
       computed waveform.
 Syntax :DISPlay:MATH:MATH<x>:SCALing?
       <x> = 1, 2 (MATH)
 Example :DISPLAY:MATH:MATH1? ->
       :DISPLAY:MATH:MATH1:SCALING:
       MODE AUTO;CENTER 0.0000E+00;
       SDIV 25.000E+00
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
```

## Page 6-34

### Left column
```text
 6.7 DISPlay Group

 :DISPlay:MATH:MATH<x>:SCALing:CENTer
 Function Sets the center value of the manual scaling of
       the computed waveform or queries the current
       setting.
 Syntax :DISPlay:MATH:MATH<x>:SCALing:
       CENTer {<NRf>}
       :DISPlay:MATH:MATH<x>:SCALing:
       CENTer?
       <x> = 1, 2 (MATH)
       <NRf> = –9.9999E+30 to 9.9999E+30
 Example :DISPLAY:MATH:MATH1:SCALING:
       CENTER 0.0000E+00
       :DISPLAY:MATH:MATH1:SCALING:CENTER?
       -> :DISPLAY:MATH:MATH1:SCALING:
       CENTER 0.0000E+00
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • This command is valid when the scaling
        mode of the computed waveform
        (:DISPlay:MATH:MATH<x>:SCALing:
        MODE) is set to “MANual.”
 :DISPlay:MATH:MATH<x>:SCALing:MODE
 Function Sets the scaling mode of the computed waveform
       or queries the current setting.
 Syntax :DISPlay:MATH:MATH<x>:SCALing:
       MODE {AUTO|MANual}
       :DISPlay:MATH:MATH<x>:SCALing:MODE?
       <x> = 1, 2 (MATH)
 Example :DISPLAY:MATH:MATH1:SCALING:
       MODE AUTO
       :DISPLAY:MATH:MATH1:SCALING:MODE?
       -> :DISPLAY:MATH:MATH1:SCALING:
       MODE AUTO
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
```
### Right column
```text
 :DISPlay:MATH:MATH<x>:SCALing:SDIV
 Function Sets the scale/division value of the manual
       scaling of the computed waveform or queries the
       current setting.
 Syntax :DISPlay:MATH:MATH<x>:SCALing:
       SDIV {<NRf>}
       :DISPlay:MATH:MATH<x>:SCALing:SDIV?
       <x> = 1, 2 (MATH)
       <NRf> = –9.9999E+30 to 9.9999E+30
 Example :DISPLAY:MATH:MATH1:SCALING:
       SDIV 2.5000E+01
       :DISPLAY:MATH:MATH1:SCALING:SDIV?
       -> :DISPLAY:MATH:MATH1:SCALING:
       SDIV 25.000E+00
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • This command is valid when the scaling
        mode of the computed waveform
        (:DISPlay:MATH:MATH<x>:SCALing:
        MODE) is set to “MANual.”
 :DISPlay:MATH:MATH<x>:UNIT
 Function Sets the unit to be added to the result of the
       waveform computation or queries the current
       setting.
 Syntax :DISPlay:MATH:MATH<x>:
       UNIT {<String>}
       :DISPlay:MATH:MATH<x>:UNIT?
       <x> = 1, 2 (MATH)
       <String> = Up to 8 characters
 Example :DISPLAY:MATH:MATH1:UNIT “W”
       :DISPLAY:MATH:MATH1:UNIT? ->
       :DISPLAY:MATH:MATH1:UNIT “W”
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
```

## Page 6-35

### Left column
```text
   :DISPlay:MODE
   Function Sets the display mode or queries the current
         setting.
   Syntax :DISPlay:MODE {NUMeric|WAVE|BAR|
         VECTor|TRENd|NWAVe|NBAR|NTRend|
         WBAR|WTRend|BTRend|MATH|NMATh|FFT|
         NFFT|WFFT|IECHarm|CBCycle|FLICker}
         :DISPlay:MODE?
         NUMeric = Displays only the numeric values.
         WAVE = Displays only the waveforms.
         BAR = Bar graph
         VECTor = Vector display
         TRENd = Trend
         NWAVe = Displays both the numeric values and
         the waveforms.
         NBAR = Displays both the numeric values and
         the bar graph.
         NTRend = Displays both the numeric values and
         the trends.
         WBAR = Displays both the waveforms and the
         bar graph.
         WTRend = Displays both the waveforms and the
         trends.
         BTRend = Displays both the bar graphs and the
         trends.
         MATH = Displays only the waveforms (including
         the computed waveforms).
         NMATh = Displays both numeric values and
         waveforms (including the computed waveforms).
         FFT = Displays only the FFT waveforms.
         NFFT = Displays both the numeric values and the
         FFT waveforms.
         WFFT = Displays both the waveforms and the
         FFT waveforms.
         IECHarm = IEC harmonic measurement mode
         display (numeric values).
         CBCycle = Cycle by Cycle mode display (value).
         FLICker = Flicker measurement mode display
         (value).
   Example :DISPLAY:MODE NUMERIC
         :DISPLAY:MODE? ->
         :DISPLAY:MODE NUMERIC
   Description • {BAR|VECTor|NBAR|WBAR|BTRend} are
          selectable only on models with the advanced
          computation function (/G6 option).
         • {MATH|NMATh|FFT|NFFT|WFFT|
          IECHarm} are selectable only on models
          with the advanced computation function (/G6
          option).
         • {FLICker} can only be selected with the
          flicker measurement function (/FL option).
```
### Right column
```text
                    6.7 DISPlay Group

 :DISPlay:NUMeric?
 Function Queries all settings related to the numeric display.
 Syntax :DISPlay:NUMeric?
 Example :DISPLAY:NUMERIC? ->
       (same as the response to
       “:DISPlay:NUMeric:NORMal?”)

 :DISPlay:NUMeric:NORMal?
 Function Queries all settings related to the numeric display.
 Syntax :DISPlay:NUMeric:NORMal?
 Example • Example in which the numeric display format
        (:DISPlay:NUMeric[:NORMal]:FORMat) is
        set to “VAL4 (4-value display)”
        :DISPLAY:NUMERIC:NORMAL? ->
        :DISPLAY:NUMERIC:NORMAL:
        FORMAT VAL4;VAL4:ITEM1 U,1,TOTAL;
        ITEM2 I,1,TOTAL;ITEM3 P,1,TOTAL;
        ...(omitted)...;ITEM35 ETA3;
        ITEM36 ETA4;CURSOR 1
       • Example in which the numeric display format
        (:DISPlay:NUMeric[:NORMal]:FORMat) is
        set to “ALL (all display)”
        :DISPLAY:NUMERIC:NORMAL? ->
        :DISPLAY:NUMERIC:NORMAL:
        FORMAT ALL;ALL:CURSOR U
 Description Returns all settings corresponding to the numeric
       display format
       (:DISPlay:NUMeric[:NORMal]:FORMat).
 :DISPlay:NUMeric[:NORMal]:ALL?
 Function Queries all settings related to the numeric display
       (all display).
 Syntax :DISPlay:NUMeric[:NORMal]:ALL?
 Example :DISPLAY:NUMERIC:NORMAL:ALL? ->
       :DISPLAY:NUMERIC:NORMAL:ALL:
       CURSOR U
 :DISPlay:NUMeric[:NORMal]:ALL:CURSor
 Function Sets the cursor position on the numeric display (all
       display) or queries the current setting.
 Syntax :DISPlay:NUMeric[:NORMal]:ALL:
       CURSor {<Function>}
       :DISPlay:NUMeric[:NORMal]:ALL:
       CURSor?
       <Function> = {U|I|P|S|Q|...} (See the
       function selection list (1) on page 6-44.)
 Example :DISPLAY:NUMERIC:NORMAL:ALL:
       CURSOR U
       :DISPLAY:NUMERIC:NORMAL:ALL:CURSOR?
       -> :DISPLAY:NUMERIC:NORMAL:ALL:
       CURSOR U
 Description Specify the cursor position in terms of the function
       name.
```

## Page 6-36

### Left column
```text
 6.7 DISPlay Group

 :DISPlay:NUMeric[:NORMal]:ALL:ORDer
 Function Sets the displayed harmonic order on the
       harmonic measurement function display page of
       the numeric display (all display) or queries the
       current setting.
 Syntax :DISPlay:NUMeric[:NORMal]:ALL:
       ORDer {<Order>}
       :DISPlay:NUMeric[:NORMal]:ALL:
       ORDer?
       <Order> = {TOTal|DC|<NRf>} (<NRf> = 1 to
       100)
 Example :DISPLAY:NUMERIC:NORMAL:ALL:ORDER 1
       :DISPLAY:NUMERIC:NORMAL:ALL:ORDER?
       -> :DISPLAY:NUMERIC:NORMAL:ALL:
       ORDER 1
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • This command is valid when
        the displayed page number
        (:DISPlay:NUMeric[:NORMal]:ALL:
        PAGE) on the numeric display (all display) is 6
        or 7.
 :DISPlay:NUMeric[:NORMal]:ALL:PAGE
 Function Sets the page number on the numeric display (all
       display) or queries the current setting.
 Syntax :DISPlay:NUMeric[:NORMal]:ALL:
       PAGE {<NRf>}
       :DISPlay:NUMeric[:NORMal]:ALL:PAGE?
       <NRf> = 1 to 5 (page number)
       <NRf> = 1 to 9 (when the advanced computation
       function (/G6 option) is installed)
 Example :DISPLAY:NUMERIC:NORMAL:ALL:PAGE 1
       :DISPLAY:NUMERIC:NORMAL:ALL:PAGE?
       -> :DISPLAY:NUMERIC:NORMAL:ALL:
       PAGE 1
 Description When the page number is set, the cursor position
       moves to the beginning of the page.
```
### Right column
```text
 :DISPlay:NUMeric[:NORMal]:FORMat
 Function Sets the numeric display format or queries the
       current setting.
 Syntax :DISPlay:NUMeric[:NORMal]:
       FORMat {VAL4|VAL8|VAL16|ALL|SINGle|
       DUAL}
       :DISPlay:NUMeric[:NORMal]:FORMat?
 Example :DISPLAY:NUMERIC:NORMAL:FORMAT VAL4
       :DISPLAY:NUMERIC:NORMAL:FORMAT? ->
       :DISPLAY:NUMERIC:NORMAL:FORMAT VAL4
 Description • The contents of the displayed numeric data are
        as follows:
        {VAL4|VAL8|VAL16}: Numeric display items
        are displayed in order by the item number. (The
        number expresses the number of items that is
        displayed on a single screen (page).)
        ALL = All functions are displayed in order by
        element.
        SINGle = One list display item is listed by
        separating the data into even and odd orders.
        DUAL = Two list display items are listed in order
        by harmonic order.
       • {SINGle|DUAL} are selectable only on
        models with the advanced computation function
        (/G6 option).
 :DISPlay:NUMeric[:NORMal]:LIST?
 Function Queries all settings related to the numeric display
       (list display).
 Syntax :DISPlay:NUMeric[:NORMal]:LIST?
 Example :DISPLAY:NUMERIC:NORMAL:LIST? ->
       :DISPLAY:NUMERIC:NORMAL:LIST:
       ITEM1 U,1;ITEM2 I,1;CURSOR ORDER;
       HEADER 1;ORDER 1
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
```

## Page 6-37

### Left column
```text
   :DISPlay:NUMeric[:NORMal]:LIST:CURS
   or
   Function Sets the cursor position on the numeric display (list
         display) or queries the current setting.
   Syntax :DISPlay:NUMeric[:NORMal]:LIST:
         CURSor {HEADer|ORDer}
         :DISPlay:NUMeric[:NORMal]:LIST:
         CURSor?
         HEADer = The cursor moves to the header
         section (data concerning all the harmonics, left
         side of the screen).
         ORDer = The cursor moves to the data section
         (Numeric data of each harmonic, right side of the
         screen).
   Example :DISPLAY:NUMERIC:NORMAL:LIST:
         CURSOR ORDER
         :DISPLAY:NUMERIC:NORMAL:LIST:
         CURSOR? -> :DISPLAY:NUMERIC:NORMAL:
         LIST:CURSOR ORDER
   Description This command is valid only on models with the
         advanced computation function (/G6 option).
   :DISPlay:NUMeric[:NORMal]:LIST:HEAD
   er
   Function Sets the cursor position in the header section on
         the numeric display (list display) or queries the
         current setting.
   Syntax :DISPlay:NUMeric[:NORMal]:LIST:
         HEADer {<NRf>}
         :DISPlay:NUMeric[:NORMal]:LIST:
         HEADer?
         <NRf> = 1 to 98
   Example :DISPLAY:NUMERIC:NORMAL:LIST:
         HEADER 1
         :DISPLAY:NUMERIC:NORMAL:LIST:
         HEADER? -> :DISPLAY:NUMERIC:NORMAL:
         LIST:HEADER 1
   Description • This command is valid only on models with the
          advanced computation function (/G6 option) .
         • This command is valid when the cursor position
          (:DISPlay:NUMeric[:NORMal]:LIST:
          CURSor) on the numeric display (list display) is
          “HEADer.”
```
### Right column
```text
                    6.7 DISPlay Group

 :DISPlay:NUMeric[:NORMal]:LIST:ITEM
 <x>
 Function Sets the displayed items (function and element)
       on the numeric display (list display) or queries the
       current setting.
 Syntax :DISPlay:NUMeric[:NORMal]:LIST:
       ITEM<x> {<Function>,<Element>}
       :DISPlay:NUMeric[:NORMal]:LIST:
       ITEM<x>?
       <x> = 1 or 2 (item number)
       <Function> = {U|I|P|S|Q|LAMBda|...} (See
       the function selection list (2) on page 6-46.)
       <Element> = {<NRf>|SIGMa|SIGMB} (<NRf>
       = 1 to 4)
 Example :DISPLAY:NUMERIC:NORMAL:LIST:
       ITEM1 U,1
       :DISPLAY:NUMERIC:NORMAL:LIST:ITEM1?
       -> :DISPLAY:NUMERIC:NORMAL:LIST:
       ITEM1 U,1
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :DISPlay:NUMeric[:NORMal]:LIST:ORDer
 Function Sets the harmonic order cursor position in the
       data section on the numeric display (list display)
       or queries the current setting.
 Syntax :DISPlay:NUMeric[:NORMal]:LIST:
       ORDer {<NRf>}
       :DISPlay:NUMeric[:NORMal]:LIST:
       ORDer?
       <NRf> = –1 to 100 (order)
 Example :DISPLAY:NUMERIC:NORMAL:LIST:
       ORDER 1
       :DISPLAY:NUMERIC:NORMAL:LIST:ORDER?
       -> :DISPLAY:NUMERIC:NORMAL:LIST:
       ORDER 1
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • This command is valid when the cursor position
        (:DISPlay:NUMeric[:NORMal]:LIST:
        CURSor) on the numeric display (list display) is
        “ORDer.”
```

## Page 6-38

### Left column
```text
 6.7 DISPlay Group

 :DISPlay:NUMeric[:NORMal]:{VAL4|VAL8
 |VAL16}?
 Function Queries all settings related to the numeric display
       ({4-value|8-value|16-value} display).
 Syntax :DISPlay:NUMeric[:NORMal]:{VAL4|
       VAL8|VAL16}?
 Example :DISPLAY:NUMERIC:NORMAL:VAL4? ->
       :DISPLAY:NUMERIC:NORMAL:VAL4:
       ITEM1 U,1,TOTAL;ITEM2 I,1,TOTAL;
       ITEM3 P,1,TOTAL;
       ITEM4 LAMBDA,1,TOTAL;
       ITEM5 U,2,TOTAL;ITEM6 I,2,TOTAL;
       ITEM7 P,2,TOTAL;
       ITEM8 LAMBDA,2,TOTAL;
       ITEM9 U,3,TOTAL;ITEM10 I,3,TOTAL;
       ITEM11 P,3,TOTAL;
       ITEM12 LAMBDA,3,TOTAL;
       ITEM13 U,4,TOTAL;ITEM14 I,4,TOTAL;
       ITEM15 P,4,TOTAL;
       ITEM16 LAMBDA,4,TOTAL;
       ITEM17 U,SIGMA,TOTAL;
       ITEM18 I,SIGMA,TOTAL;
       ITEM19 P,SIGMA,TOTAL;
       ITEM20 LAMBDA,SIGMA,TOTAL;
       ITEM21 U,SIGMB,TOTAL;
       ITEM22 I,SIGMB,TOTAL;
       ITEM23 P,SIGMB,TOTAL;
       ITEM24 LAMBDA,SIGMB,TOTAL;
       ITEM25 WH,1;ITEM26 WH,2;
       ITEM27 WH,3;ITEM28 WH,4;
       ITEM29 WH,SIGMA;ITEM30 WH,SIGMB;
       ITEM31 F1;ITEM32 F2;ITEM33 ETA1;
       ITEM34 ETA2;ITEM35 ETA3;
       ITEM36 ETA4;CURSOR 1
 :DISPlay:NUMeric[:NORMal]:{VAL4|VAL8
 |VAL16}:CURSor
 Function Sets the cursor position on the numeric display
       ({4-value|8-value|16-value} display) or queries the
       current setting.
 Syntax :DISPlay:NUMeric[:NORMal]:{VAL4|
       VAL8|VAL16}:CURSor {<NRf>}
       :DISPlay:NUMeric[:NORMal]:{VAL4|
       VAL8|VAL16}:CURSor?
       <NRf> = 1 to 36 (item number, for VAL4)
       <NRf> = 1 to 72 (item number, for VAL8)
       <NRf> = 1 to 144 (item number, for VAL16)
 Example :DISPLAY:NUMERIC:NORMAL:VAL4:
       CURSOR 1
       :DISPLAY:NUMERIC:NORMAL:VAL4:
       CURSOR? -> :DISPLAY:NUMERIC:NORMAL:
       VAL4:CURSOR 1
 Description Specify the cursor position in terms of the item
       number.
```
### Right column
```text
 :DISPlay:NUMeric[:NORMal]:{VAL4|VAL8
 |VAL16}:ITEM<x>
 Function Sets the displayed items (function, element,
       and harmonic order) on the numeric display
       ({4-value|8-value|16-value} display) or queries the
       current setting.
 Syntax :DISPlay:NUMeric:[:NORMal]:{VAL4|
       VAL8|VAL16}:ITEM<x> {NONE|
       <Function>,<Element>[,<Order>]}
       :DISPlay:NUMeric:[:NORMal]:{VAL4|
       VAL8|VAL16}:ITEM<x>?
       <x> = 1 to 36 (item number, for VAL4)
       <x> = 1 to 72 (item number, for VAL8)
       <x> = 1 to 144 (item number, for VAL16)
       NONE = No display item
       <Function> = {U|I|P|S|Q|...} (See the
       function selection list (1) on page 6-44.)
       <Element> = {<NRf>|SIGMa|SIGMB} (<NRf>
       = 1 to 4)
       <Order> = {TOTal|DC|<NRf>} (<NRf> = 1 to
       100)
 Example :DISPLAY:NUMERIC:NORMAL:VAL4:
       ITEM1 U,1,TOTAL
       :DISPLAY:NUMERIC:NORMAL:VAL4:ITEM1?
       -> :DISPLAY:NUMERIC:NORMAL:VAL4:
       ITEM1 U,1,TOTAL
 Description • If <Element> is omitted, element 1 is set.
       • If <Order> is omitted, TOTal is set.
       • <Element> or <Order> is omitted from
        response to functions that do not need them.
 :DISPlay:NUMeric[:NORMal]:{VAL4|VAL8
 |VAL16}:PAGE
 Function Sets the page number on the numeric display
       ({4-value|8-value|16-value} display) or queries the
       current setting.
 Syntax :DISPlay:NUMeric[:NORMal]:{VAL4|
       VAL8|VAL16}:PAGE {<NRf>}
       :DISPlay:NUMeric[:NORMal]:{VAL4|
       VAL8|VAL16}:PAGE?
       <NRf> = 1 to 9 (page number)
 Example :DISPLAY:NUMERIC:NORMAL:VAL4:PAGE 1
       :DISPLAY:NUMERIC:NORMAL:VAL4:PAGE?
       -> :DISPLAY:NUMERIC:NORMAL:VAL4:
       PAGE 1
 Description When the page number is set, the cursor position
       moves to the beginning of the page.
```

## Page 6-39

### Left column
```text
   :DISPlay:NUMeric[:NORMal]:{VAL4|VAL8
   |VAL16}:PRESet
   Function Sets the displayed items on the numeric display
         ({4-value|8-value|16-value} display) to a preset
         pattern.
   Syntax :DISPlay:NUMeric[:NORMal]:{VAL4|
         VAL8|VAL16}:PRESet {<NRf>}
         <NRf> = 1 to 4
   Example :DISPLAY:NUMERIC:NORMAL:VAL4:
         PRESET 1
   Description Regardless of what value (1 to 4) is specified
         for <NRf>, the display pattern (order) of the
         numeric display items will be the same as the
         display order when Reset Items Exec of the ITEM
         setting menu, which is displayed on the screen,
         is executed. For details on the order of displayed
         items when reset is executed, see the User’s
         Manual IM WT3001E-01EN.
   :DISPlay:TRENd?
   Function Queries all settings related to the trend.
   Syntax :DISPlay:TRENd?
   Example :DISPLAY:TREND? -> :DISPLAY:TREND:
         FORMAT SINGLE;T1 1;T2 1;T3 1;T4 1;
         T5 1;T6 1;T7 1;T8 1;T9 0;T10 0;
         T11 0;T12 0;T13 0;T14 0;T15 0;
         T16 0;TDIV 0,0,3;ITEM1:
         FUNCTION U,1,TOTAL;SCALING:
         MODE AUTO;
         VALUE 100.0E+00,-100.0E+00;:
         DISPLAY:TREND:ITEM2:
         FUNCTION I,1,TOTAL;SCALING:
         MODE AUTO;
         VALUE 100.0E+00,-100.0E+00;...
         (omitted)...;:DISPLAY:TREND:NORMAL:
         ITEM16:FUNCTION AH,1;SCALING:
         MODE AUTO;
         VALUE 100.0E+00,-100.0E+00
   :DISPlay:TRENd:ALL
   Function Collectively turns ON/OFF all trends.
   Syntax :DISPlay:TRENd:ALL {<Boolean>}
   Example :DISPLAY:TREND:ALL ON
   :DISPlay:TRENd:CLEar
   Function Clears the trend.
   Syntax :DISPlay:TRENd:CLEar
   Example :DISPLAY:TREND:CLEAR
```
### Right column
```text
                    6.7 DISPlay Group

 :DISPlay:TRENd:FORMat
 Function Sets the display format of the trend or queries the
       current setting.
 Syntax :DISPlay:TRENd:FORMat {SINGle|DUAL|
       TRIad|QUAD}
       :DISPlay:TRENd:FORMat?
 Example :DISPLAY:TREND:FORMAT SINGLE
       :DISPLAY:TREND:FORMAT? ->
       :DISPLAY:TREND:FORMAT SINGLE
 :DISPlay:TRENd:ITEM<x>?
 Function Queries all settings related to the trend.
 Syntax :DISPlay:TRENd:ITEM<x>?
       <x> = 1 to 16 (item number)
 Example :DISPLAY:TREND:ITEM1? -> :DISPLAY:
       TREND:ITEM1:FUNCTION U,1,TOTAL;
       SCALING:MODE AUTO;
       VALUE 100.0E+00,-100.0E+00

 :DISPlay:TRENd:ITEM<x>[:FUNCtion]
 Function Sets the trend item (function, element, and
       harmonic order) or queries the current setting.
 Syntax :DISPlay:TRENd:ITEM<x>
       [:FUNCtion] {NONE|<Function>,
       <Element>[,<Order>]}
       :DISPlay:TRENd:ITEM<x>:FUNCtion?
       <x> = 1 to 16 (item number)
       NONE = No display item
       <Function> = {U|I|P|S|Q|...} (See the
       function selection list (1) on page 6-44.)
       <Element> = {<NRf>|SIGMa|SIGMB} (<NRf>
       = 1 to 4)
       <Order> = {TOTal|DC|<NRf>} (<NRf> = 1 to
       100)
 Example :DISPLAY:TREND:ITEM1:
       FUNCTION U,1,TOTAL
       :DISPLAY:TREND:ITEM1:FUNCTION? ->
       :DISPLAY:TREND:ITEM1:
       FUNCTION U,1,TOTAL
 Description • If <Element> is omitted, element 1 is set.
       • If <Order> is omitted, TOTal is set.
       • <Element> or <Order> is omitted from
        response to functions that do not need them.
 :DISPlay:TRENd:ITEM<x>:SCALing?
 Function Queries all settings related to the scaling of the
       trend.
 Syntax :DISPlay:TRENd:ITEM<x>:SCALing?
       <x> = 1 to 16 (item number)
 Example :DISPLAY:TREND:ITEM1:SCALING? ->
       :DISPLAY:TREND:ITEM1:SCALING:
       MODE AUTO;
       VALUE 100.0E+00,-100.0E+00
```

## Page 6-40

### Left column
```text
 6.7 DISPlay Group

 :DISPlay:TRENd:ITEM<x>:SCALing:MODE
 Function Sets the scaling mode of the trend or queries the
       current setting.
 Syntax :DISPlay:TRENd:ITEM<x>:SCALing:
       MODE {AUTO|MANual}
       :DISPlay:TRENd:ITEM<x>:SCALing:
       MODE?
       <x> = 1 to 16 (item number)
 Example :DISPLAY:TREND:ITEM1:SCALING:
       MODE AUTO
       :DISPLAY:TREND:ITEM1:SCALING:MODE?
       -> :DISPLAY:TREND:ITEM1:SCALING:
       MODE AUTO
 :DISPlay:TRENd:ITEM<x>:SCALing:VALue
 Function Sets the upper and lower limits of manual scaling
       of the trend or queries the current setting.
 Syntax :DISPlay:TRENd:ITEM<x>:SCALing:
       VALue {<NRf>,<NRf>}
       :DISPlay:TRENd:ITEM<x>:SCALing:
       VALue?
       <x> = 1 to 16 (item number)
       <NRf> = –9.999E+30 to 9.999E+30
 Example :DISPLAY:TREND:ITEM1:SCALING:
       VALUE 100,-100
       :DISPLAY:TREND:ITEM1:SCALING:VALUE?
       -> :DISPLAY:TREND:ITEM1:SCALING:
       VALUE 100.0E+00,-100.0E+00
 Description • Set the upper limit and then the lower limit.
       • This command is valid when the scaling mode
        of the trend
        (:DISPlay:TRENd:ITEM<x>:SCALing:
        MODE) is set to “MANual.”
 :DISPlay:TRENd:TDIV
 Function Sets the horizontal axis (T/div) of the trend or
       queries the current setting.
 Syntax :DISPlay:TRENd:TDIV {<NRf>,<NRf>,
       <NRf>}
       :DISPlay:TRENd:TDIV?
       {<NRf>, <NRf>, <NRf>} = 0, 0, 3 to 24, 0, 0
       1st <NRf> = 1, 3, 6, 12, 24 (hour)
       2nd <NRf> = 1, 3, 6, 10, 30 (minute)
       3rd <NRf> = 3, 6, 10, or 30 (second)
 Example :DISPLAY:TREND:TDIV 0,0,3
       :DISPLAY:TREND:TDIV? ->
       :DISPLAY:TREND:TDIV 0,0,3
 Description Set the three <NRf>’s so that one <NRf> is a
       non-zero value and the other two are zeroes.
```
### Right column
```text
 :DISPlay:TRENd:T<x>
 Function Turns ON/OFF the trend or queries the current
       setting.
 Syntax :DISPlay:TRENd:T<x> {<Boolean>}
       :DISPlay:TRENd:T<x>?
       <x> = 1 to 16 (item number)
 Example :DISPLAY:TREND:T1 ON
       :DISPLAY:TREND:T1? ->
       :DISPLAY:TREND:T1 1
 :DISPlay:VECTor?
 Function Queries all settings related to the vector display.
 Syntax :DISPlay:VECTor?
 Example :DISPLAY:VECTOR? -> :DISPLAY:
       VECTOR:OBJECT SIGMA;NUMERIC 1;
       UMAG 1.000;IMAG 1.000
 Description This command is valid only on models with the
       advanced computation function (/G6 option).

 :DISPlay:VECTor:NUMeric
 Function Turns ON/OFF the numeric data display for the
       vector display or queries the current setting.
 Syntax :DISPlay:VECTor:NUMeric {<Boolean>}
       :DISPlay:VECTor:NUMeric?
 Example :DISPLAY:VECTOR:NUMERIC ON
       :DISPLAY:VECTOR:NUMERIC? ->
       :DISPLAY:VECTOR:NUMERIC 1
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :DISPlay:VECTor:OBJect
 Function Sets the wiring unit to be displayed during vector
       display or queries the current setting.
 Syntax :DISPlay:VECTor:OBJect {SIGMA|
       SIGMB}
       :DISPlay:VECTor:OBJect?
 Example :DISPLAY:VECTOR:OBJECT SIGMA
       :DISPLAY:VECTOR:OBJECT? ->
       :DISPLAY:VECTOR:OBJECT SIGMA
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • SIGMB is selectable only on the 4-element
        model.
```

## Page 6-41

### Left column
```text
   :DISPlay:VECTor:{UMAG|IMAG}
   Function Sets the zoom factor of the {voltage|current}
         display during vector display or queries the
         current setting.
   Syntax :DISPlay:VECTor:{UMAG|IMAG} {<NRf>}
         :DISPlay:VECTor:{UMAG|IMAG}?
         <NRf> = 0.100 to 100.000
   Example :DISPLAY:VECTOR:UMAG 1
         :DISPLAY:VECTOR:UMAG? ->
         :DISPLAY:VECTOR:UMAG 1.000
   Description This command is valid only on models with the
         advanced computation function (/G6 option).
   :DISPlay:WAVE?
   Function Queries all settings related to the waveform
         display.
   Syntax :DISPlay:WAVE?
   Example :DISPLAY:WAVE? -> :DISPLAY:WAVE:
         FORMAT SINGLE;U1 1;U2 1;U3 1;U4 1;
         I1 1;I2 1;I3 1;I4 1;TDIV 5.0E-03;
         TRIGGER:MODE AUTO;SOURCE U1;
         SLOPE RISE;LEVEL 0.0;:DISPLAY:WAVE:
         INTERPOLATE LINE;GRATICULE GRID;
         SVALUE 1;TLABEL 0;MAPPING:
         MODE AUTO;:DISPLAY:WAVE:VZOOM:
         U1 1.00;U2 1.00;U3 1.00;U4 1.00;
         I1 1.00;I2 1.00;I3 1.00;I4 1.00;:
         DISPLAY:WAVE:POSITION:U1 0.000;
         U2 0.000;U3 0.000;U4 0.000;
         I1 0.000;I2 0.000;I3 0.000;I4 0.000
   :DISPlay:WAVE:ALL
   Function Collectively turns ON/OFF all waveform displays.
   Syntax :DISPlay:WAVE:ALL {<Boolean>}
   Example :DISPLAY:WAVE:ALL ON
   :DISPlay:WAVE:FORMat
   Function Sets the display format of the waveform or
         queries the current setting.
   Syntax :DISPlay:WAVE:FORMat {SINGle|DUAL|
         TRIad|QUAD}
         :DISPlay:WAVE:FORMat?
   Example :DISPLAY:WAVE:FORMAT SINGLE
         :DISPLAY:WAVE:FORMAT? ->
         :DISPLAY:WAVE:FORMAT SINGLE
```
### Right column
```text
                    6.7 DISPlay Group

 :DISPlay:WAVE:GRATicule
 Function Sets the graticule (grid) type or queries the
       current setting.
 Syntax :DISPlay:WAVE:GRATicule {GRID|
       FRAMe|CROSshair}
       :DISPlay:WAVE:GRATicule?
 Example :DISPLAY:WAVE:GRATICULE GRID
       :DISPLAY:WAVE:GRATICULE? ->
       :DISPLAY:WAVE:GRATICULE GRID
 :DISPlay:WAVE:INTerpolate
 Function Sets the interpolation method of the waveform or
       queries the current setting.
 Syntax :DISPlay:WAVE:INTerpolate {OFF|
       LINE}
       :DISPlay:WAVE:INTerpolate?
 Example :DISPLAY:WAVE:INTERPOLATE LINE
       :DISPLAY:WAVE:INTERPOLATE? ->
       :DISPLAY:WAVE:INTERPOLATE LINE

 :DISPlay:WAVE:MAPPing?
 Function Queries all settings related to the waveform
       mapping to the split screen.
 Syntax :DISPlay:WAVE:MAPPing?
 Example :DISPLAY:WAVE:MAPPING? ->
       :DISPLAY:WAVE:MAPPING:MODE USER;
       U1 0;U2 1;U3 2;U4 3;I1 0;I2 1;I3 2;
       I4 3
 :DISPlay:WAVE:MAPPing[:MODE]
 Function Sets the waveform mapping method for the split
       screen or queries the current setting.
 Syntax :DISPlay:WAVE:MAPPing[:MODE] {AUTO|
       FIXed|USER}
       :DISPlay:WAVE:MAPPing:MODE?
 Example :DISPLAY:WAVE:MAPPING:MODE AUTO
       :DISPLAY:WAVE:MAPPING:MODE? ->
       :DISPLAY:WAVE:MAPPING:MODE AUTO
```

## Page 6-42

### Left column
```text
 6.7 DISPlay Group

 :DISPlay:WAVE:MAPPing:{U<x>|I<x>|SPE
 ed|TORQue|MATH<x>}
 Function Sets the mapping of the {voltage|current|rotating
       speed|torque|waveform computation} waveform
       to the split screen or queries the current setting.
 Syntax :DISPlay:WAVE:MAPPing:{U<x>|I<x>|
       SPEed|TORQue|MATH<x>} {<NRf>}
       :DISPlay:WAVE:MAPPing:{U<x>|I<x>|
       SPEed|TORQue|MATH<x>}?
       <x> of U<x>, I<x> = 1 to 4 (element)
       <x> of MATH<x> = 1 to 2 (MATH)
       <NRf> = 0 to 3
 Example :DISPLAY:WAVE:MAPPING:U1 0
       :DISPLAY:WAVE:MAPPING:U1? ->
       :DISPLAY:WAVE:MAPPING:U1 0
 Description • This command is valid when the waveform
        mapping method (:DISPlay:WAVE:
        MAPPing[:MODE]) is set to “USER.”
       • {SPEed|TORQue} are valid only on models
        with the motor evaluation function (/MTR
        option).
       • MATH<x> is valid only on models with the
        advanced computation function (/G6 option).
 :DISPlay:WAVE:POSition?
 Function Queries all settings related to the vertical position
       (level of the center position) of the waveform.
 Syntax :DISPlay:WAVE:POSition?
 Example :DISPLAY:WAVE:POSITION? ->
       :DISPLAY:WAVE:POSITION:U1 0.000;
       U2 0.000;U3 0.000;U4 0.000;
       I1 0.000;I2 0.000;I3 0.000;I4 0.000
 :DISPlay:WAVE:POSition:{UALL|IALL}
 Function Collectively sets the vertical position (level of the
       center position) of the waveform {voltage|current}
       of all elements.
 Syntax :DISPlay:WAVE:POSition:{UALL|
       IALL} {<NRf>}
       <NRf> = –130.000 to 130.000(%)
 Example :DISPLAY:WAVE:POSITION:UALL 0
 :DISPlay:WAVE:POSition:{U<x>|I<x>}
 Function Sets the vertical position (level of the center
       position) of the waveform {voltage|current} of the
       element or queries the current setting.
 Syntax :DISPlay:WAVE:POSition:{U<x>|
       I<x>} {<NRf>}
       :DISPlay:WAVE:POSition:{U<x>|I<x>}?
       <x> = 1 to 4 (element)
       <NRf> = –130.000 to 130.000(%)
 Example :DISPLAY:WAVE:POSITION:U1 0
       :DISPLAY:WAVE:POSITION:U1? ->
       :DISPLAY:WAVE:POSITION:U1 0.000
```
### Right column
```text
 :DISPlay:WAVE:SVALue (Scale VALue)
 Function Turns ON/OFF the scale value display or queries
       the current setting.
 Syntax :DISPlay:WAVE:SVALue {<Boolean>}
       :DISPlay:WAVE:SVALue?
 Example :DISPLAY:WAVE:SVALUE ON
       :DISPLAY:WAVE:SVALUE? ->
       :DISPLAY:WAVE:SVALUE 1
 :DISPlay:WAVE:TDIV
 Function Sets the Time/div value of the waveform or
       queries the current setting.
 Syntax :DISPlay:WAVE:TDIV {<Time>}
       :DISPlay:WAVE:TDIV?
       <Time> = 0.5, 1, 2, 5, 10, 20, 50, 100, 200, 500
       (ms), 1, or 2 (s)
 Example :DISPLAY:WAVE:TDIV 5MS
       :DISPLAY:WAVE:TDIV? ->
       :DISPLAY:WAVE:TDIV 5.0E-03
 Description The specifiable Time/div value is up to 1/10 of the
       data update interval (:RATE).
 :DISPlay:WAVE:TLABel (Trace LABel)
 Function Turns ON/OFF the waveform label display or
       queries the current setting.
 Syntax :DISPlay:WAVE:TLABel {<Boolean>}
       :DISPlay:WAVE:TLABel?
 Example :DISPLAY:WAVE:TLABEL OFF
       :DISPLAY:WAVE:TLABEL? ->
       :DISPLAY:WAVE:TLABEL 0

 :DISPlay:WAVE:TRIGger?
 Function Queries all settings related to the trigger.
 Syntax :DISPlay:WAVE:TRIGger?
 Example :DISPLAY:WAVE:TRIGGER? ->
       :DISPLAY:WAVE:TRIGGER:MODE AUTO;
       SOURCE U1;SLOPE RISE;LEVEL 0.0
 :DISPlay:WAVE:TRIGger:LEVel
 Function Sets the trigger level or queries the current
       setting.
 Syntax :DISPlay:WAVE:TRIGger:LEVel {<NRf>}
       :DISPlay:WAVE:TRIGger:LEVel?
       <NRf> = –100.0 to 100.0 (%) (The resolution is
       0.1(%))
 Example :DISPLAY:WAVE:TRIGGER:LEVEL 0
       :DISPLAY:WAVE:TRIGGER:LEVEL? ->
       :DISPLAY:WAVE:TRIGGER:LEVEL 0.0
 Description Set the value in terms of a percentage of the full
       scale value displayed on the screen.
```

## Page 6-43

### Left column
```text
   :DISPlay:WAVE:TRIGger:MODE
   Function Sets the trigger mode or queries the current
         setting.
   Syntax :DISPlay:WAVE:TRIGger:MODE {AUTO|
         NORMal|OFF}
         :DISPlay:WAVE:TRIGger:MODE?
   Example :DISPLAY:WAVE:TRIGGER:MODE AUTO
         :DISPLAY:WAVE:TRIGGER:MODE? ->
         :DISPLAY:WAVE:TRIGGER:MODE AUTO
   :DISPlay:WAVE:TRIGger:SLOPe
   Function Sets the trigger slope or queries the current
         setting.
   Syntax :DISPlay:WAVE:TRIGger:SLOPe {RISE|
         FALL|BOTH}
         :DISPlay:WAVE:TRIGger:SLOPe?
   Example :DISPLAY:WAVE:TRIGGER:SLOPE RISE
         :DISPLAY:WAVE:TRIGGER:SLOPE? ->
         :DISPLAY:WAVE:TRIGGER:SLOPE RISE

   :DISPlay:WAVE:TRIGger:SOURce
   Function Sets the trigger source or queries the current
         setting.
   Syntax :DISPlay:WAVE:TRIGger:SOURce {U<x>|
         I<x>|EXTernal}
         :DISPlay:WAVE:TRIGger:SOURce?
         <x> = 1 to 4 (element)
         EXTernal = External trigger input (Ext Clk)
   Example :DISPLAY:WAVE:TRIGGER:SOURCE U1
         :DISPLAY:WAVE:TRIGGER:SOURCE? ->
         :DISPLAY:WAVE:TRIGGER:SOURCE U1
   :DISPlay:WAVE:{U<x>|I<x>|SPEed|TORQu
   e|MATH<x>}
   Function Turns ON/OFF the {voltage|current|rotating
         speed|torque|waveform computation} waveform
         or queries the current setting.
   Syntax :DISPlay:WAVE:{U<x>|I<x>|SPEed|
         TORQue|MATH<x>} {<Boolean>}
         :DISPlay:WAVE:{U<x>|I<x>|SPEed|
         TORQue|MATH<x>}?
         <x> of U<x>, I<x> = 1 to 4 (element)
         <x> of MATH<x> = 1 to 2 (MATH)
   Example :DISPLAY:WAVE:U1 ON
         :DISPLAY:WAVE:U1? -> :DISPLAY:WAVE:U1
         1
   Description • {SPEed|TORQue} are valid only on models
          with the motor evaluation function (/MTR
          option).
         • MATH<x> is valid only on models with the
          advanced computation function (/G6 option).
```
### Right column
```text
                    6.7 DISPlay Group

 :DISPlay:WAVE:VZoom?
 Function Queries all settings related to the vertical zoom
       factor of the waveform.
 Syntax :DISPlay:WAVE:VZoom?
 Example :DISPLAY:WAVE:VZOOM? ->
       :DISPLAY:WAVE:VZOOM:U1 1.00;
       U2 1.00;U3 1.00;U4 1.00;I1 1.00;
       I2 1.00;I3 1.00;I4 1.00
 :DISPlay:WAVE:VZoom:{UALL|IALL}
 Function Collectively sets the vertical zoom factor of the
       waveform {voltage|current} of all elements.
 Syntax :DISPlay:WAVE:VZoom:{UALL|IALL}
       {<NRf>}
       <NRf> = 0.1 to 100 (see the User’s Manual IM
       WT3001E-01EN)
 Example :DISPLAY:WAVE:VZOOM:UALL 1

 :DISPlay:WAVE:VZoom:{U<x>|I<x>}
 Function Sets the vertical zoom factor of the waveform
       {voltage|current} of the element or queries the
       current setting.
 Syntax :DISPlay:WAVE:VZoom:{U<x>|I<x>}
       {<NRf>}
       :DISPlay:WAVE:VZoom:{U<x>|I<x>}?
       <x> = 1 to 4 (element)
       <NRf> = 0.1 to 100 (see the User’s Manual IM
       WT3001E-01EN)
 Example :DISPLAY:WAVE:VZOOM:U1 1
       :DISPLAY:WAVE:VZOOM:U1? ->
       :DISPLAY:WAVE:VZOOM:U1 1.00
```

## Page 6-44

```text
 6.7 DISPlay Group

  *Function Selection (<Function>) List
               (1) Function of numeric data
                  Applicable commands
                  :AOUTput[:NORMal]:CHANnel<x>
                  :DISPlay:NUMeric[:NORMal]:{VAL4|VAL8|VAL16}:ITEM<x>
                  :DISPlay:TRENd:ITEM<x>[:FUNCtion]
                  :NUMeric[:NORMal]:ITEM<x>
                   Function name used Function name used Elements Order
                   in commands on the menu
                              (Numeric display header name)
                   U          U (Urms/Umn/Udc/Urmn) Required Required
                   I          I (Irms/Imn/Idc/Irmn) Required Required
                   P          P                 Required Required
                   S          S                 Required Required
                   Q          Q                 Required Required
                   LAMBda     λ                 Required Required
                   PHI        φ                 Required Required
                   FU         FreqU (fU)        Required Not required
                   FI         FreqI (fI)        Required Not required
                   UPPeak     U+peak (U+pk)     Required Not required
                   UMPeak     U-peak (U-pk)     Required Not required
                   IPPeak     I+peak (I+pk)     Required Not required
                   IMPeak     I-peak (I-pk)     Required Not required
                   CFU        CfU               Required Not required
                   CFI        CfI               Required Not required
                   PC         Pc                Required Not required
                   TIME       Time              Required Not required
                   WH         WP                Required Not required
                   WHP        WP+               Required Not required
                   WHM        WP-               Required Not required
                   AH         q                 Required Not required
                   AHP        q+                Required Not required
                   AHM        q-                Required Not required
                   WS         WS                Required Not required
                   WQ         WQ                Required Not required
                   ETA1       η1                Not required Not required
                   ETA2       η2                Not required Not required
                   ETA3       η3                Not required Not required
                   ETA4       η4                Not required Not required
                   DELTA1     ∆F1               Not required Not required
                   DELTA2     ∆F2               Not required Not required
                   DELTA3     ∆F3               Not required Not required
                   DELTA4     ∆F4               Not required Not required
                   F1         F1                Not required Not required
                   F2         F2                Not required Not required
                   F3         F3                Not required Not required
                   F4         F4                Not required Not required
                   F5         F5                Not required Not required
                   F6         F6                Not required Not required
                   F7         F7                Not required Not required
                   F8         F8                Not required Not required
                   F9         F9                Not required Not required
                   F10        F10               Not required Not required
                   F11        F11               Not required Not required
                   F12        F12               Not required Not required
                   F13        F13               Not required Not required
                   F14        F14               Not required Not required
                   F15        F15               Not required Not required
                   F16        F16               Not required Not required
                   F17        F17               Not required Not required
                   F18        F18               Not required Not required
                   F19        F19               Not required Not required
                   F20        F20               Not required Not required
```

## Page 6-45

```text
                                                         6.7 DISPlay Group

                     Functions that require the advanced computation function (/G6 option)
                     PHIU       φU          Required    Required
                     PHII       φI          Required    Required
                     Z          Z           Required    Required
                     RS         Rs          Required    Required
                     XS         Xs          Required    Required
                     RP         Rp          Required    Required
                     XP         Xp          Required    Required
                     UHDF       Uhdf        Required    Required
                     IHDF       Ihdf        Required    Required
                     PHDF       Phdf        Required    Required
                     UTHD       Uthd        Required    Not required
                     ITHD       Ithd        Required    Not required
                     PTHD       Pthd        Required    Not required
                     UTHF       Uthf        Required    Not required
                     ITHF       Ithf        Required    Not required
                     UTIF       Utif        Required    Not required
                     ITIF       Itif        Required    Not required
                     HVF        hvf         Required    Not required
                     HCF        hcf         Required    Not required
                     PHI_U1U2   φUi-Uj      Required    Not required
                     PHI_U1U3   φUi-Uk      Required    Not required
                     PHI_U1I1   φUi-Ii      Required    Not required
                     PHI_U1I2   φUi-Ij      Required    Not required
                     PHI_U1I3   φUi-Ik      Required    Not required
                     Functions that require the motor evaluation function (/MTR option)
                     SPEed      Speed       Not required Not required
                     TORQue     Torque      Not required Not required
                     SYNCsp     SyncSp      Not required Not required
                     SLIP       Slip        Not required Not required
                     PM         Pm          Not required Not required
```

## Page 6-46

```text
 6.7 DISPlay Group

                   In addition, the function listed below can be used for the following command.
                   :DISPlay:NUMeric[:NORMal]:ALL:CURSor
                   :FILE:SAVE:NUMeric[:NORMal]:<Function>
                   :HCOPy:PRINter:LIST[:NORMal]:<Function>
                   :STORe:NUMeric[:NORMal]:<Function>
                   Functions that require the advanced computation function (/G6 option)
                   UK             U(k)
                   IK             I(k)
                   PK             P(k)
                   SK             S(k)
                   QK             Q(k)
                   LAMBDAK        λ(k)
                   PHIK           φ(k)
                   PHIUk          φU(k)
                   PHIIk          φI(k)
                   Zk             Z(k)
                   RSk            Rs(k)
                   XSk            Xs(k)
                   RPk            Rp(k)
                   XPk            Xp(k)
                 Note
                  • For functions that do not require the element to be specified in the selection list above, set the
                    parameter to 1 or omit the parameter for commands that have a parameter for specifying the
                    element (<Element>).
                  • Likewise, for functions that do not require the harmonic order to be specified, set the
                    parameter to “TOTal” or omit the parameter for commands that have a parameter for
                    specifying the harmonic order (<Order>).
               (2) Functions of the numeric list data (The advanced computation function (/
                  G6 option) is required.)
                  Applicable commands
                  :DISPlay:BAR:ITEM<x>
                  :DISPlay:NUMeric[:NORMal]:LIST:ITEM<x>
                   Function name used Function name used
                   in commands    on the menu
                                  (Numeric display header name)
                   U              U
                   I              I
                   P              P
                   S              S
                   Q              Q
                   LAMBda         λ
                   PHI            φ
                   PHIU           φU
                   PHII           φI
                   Z              Z
                   RS             Rs
                   XS             Xs
                   RP             Rp
                   XP             Xp
                   In addition, the function listed below can be used for the following command.
                   :NUMeric:LIST:ITEM<x>
                   UHDF           Uhdf
                   IHDF           Ihdf
                   PHDF           Phdf
```

## Page 6-47

### Section introduction
```text
     6.8    FILE  Group

   The commands in this group deal with file operations.
   You can make the same settings and inquiries as when FILE on the front panel is used.
```
### Left column
```text
   :FILE?
   Function Queries all settings related to the file operation.
   Syntax :FILE?
   Example :FILE? -> (same as the response to
         “:FILE:SAVE?”)

   :FILE:CDIRectory
   Function Changes the current directory.
   Syntax :FILE:CDIRectory {<Filename>}
         <Filename> = Directory name
   Example :FILE:CDIRECTORY “IMAGE”
   Description Specify “..” to move up to the parent directory.
   :FILE:DELete:IMAGe:{TIFF|BMP|PSCRipt
   |PNG|JPEG}
   Function Deletes the screen image data file.
   Syntax :FILE:DELete:IMAGe:{TIFF|BMP|
         PSCRipt|PNG|JPEG} {<Filename>}
   Example :FILE:DELETE:IMAGE:TIFF “IMAG1”
   Description Specify the file name without the extension.

   :FILE:DELete:NUMeric:{ASCii|FLOat}
   Function Deletes the numeric data file.
   Syntax :FILE:DELete:NUMeric:{ASCii|
         FLOat} {<Filename>}
   Example :FILE:DELETE:NUMERIC:ASCII “NUM1”
   Description Specify the file name without the extension.
   :FILE:DELete:SETup
   Function Deletes the setup parameter file.
   Syntax :FILE:DELete:SETup {<Filename>}
   Example :FILE:DELETE:SETUP “SETUP1”
   Description Specify the file name without the extension.

   :FILE:DELete:WAVE:{BINary|ASCii|FLOat}
   Function Deletes the waveform display data file.
   Syntax :FILE:DELete:WAVE:{BINary|ASCii|
         FLOat} {<Filename>}
   Example :FILE:DELETE:WAVE:BINARY “WAVE1”
   Description Specify the file name without the extension.
```
### Right column
```text
 :FILE:DRIVe
 Function Sets the target drive.
 Syntax :FILE:DRIVe {PCCard[,<NRf>]|
       NETWork|USB,<NRf>[,<NRf>][,<NRf>]}
       PCCard = PC card drive
       <NRf> = Partition (0 to 3)
       NETWork = Network drive
       USB = USB memory drive
       1st <NRf> = ID number (address)
       2nd <NRf> = Partition (0 to 3) or LUN (logical unit
       number: 0 to 3)
       3rd <NRf> = Partition (0 to 3) when LUN is
       specified
 Example :FILE:DRIVE PCCARD
 Description • If the drive does not contain partitions, omit the
        <NRf> corresponding to partitions.
       • “NETWork” can be used when the Ethernet
        interface (/C7 option) is installed.
       • “USB” can be used when the USB port
        (peripheral device) (/C5 option) is installed.
       • The second or third <NRf> when USB is
        selected can be omitted if the drive is not
        partitioned or divided by LUN.
 :FILE:FORMat:EXECute
 Function Formats the PC card.
 Syntax :FILE:FORMat:EXECute
 Example :FILE:FORMAT:EXECUTE
 :FILE:FREE?
 Function Queries the free disk space (bytes) on the drive.
 Syntax :FILE:FREE?
 Example :FILE:FREE? -> 163840

 :FILE:LOAD:ABORt
 Function Aborts file loading.
 Syntax :FILE:LOAD:ABORt
 Example :FILE:LOAD:ABORT
 :FILE:LOAD:SETup
 Function Loads the setup parameter file.
 Syntax :FILE:LOAD:SETup {<Filename>}
 Example :FILE:LOAD:SETUP “SETUP1”
 Description • Specify the file name without the extension.
       • This command is an overlap command.
```

## Page 6-48

### Left column
```text
 6.8 FILE Group

 :FILE:MDIRectory
 Function Creates a directory.
 Syntax :FILE:MDIRectory {<Filename>}
       <Filename> = Directory name
 Example :FILE:MDIRECTORY “TEST”

 :FILE:PATH?
 Function Queries the absolute path of the current directory.
 Syntax :FILE:PATH?
 Example :FILE:PATH? -> “PC_Card\IMAGE”
 :FILE:SAVE?
 Function Queries all settings related to the saving of files.
 Syntax :FILE:SAVE?
 Example :FILE:SAVE? -> :FILE:SAVE:
       ANAMING 1;COMMENT “”;WAVE:
       TYPE BINARY;:FILE:SAVE:NUMERIC:
       TYPE ASCII;NORMAL:ELEMENT1 1;
       ELEMENT2 0;ELEMENT3 0;ELEMENT4 0;
       SIGMA 0;SIGMB 0;U 1;I 1;P 1;S 1;
       Q 1;LAMBDA 1;PHI 1;FU 1;FI 1;
       UPPEAK 0;UMPEAK 0;IPPEAK 0;
       IMPEAK 0;CFU 0;CFI 0;PC 0;TIME 0;
       WH 0;WHP 0;WHM 0;AH 0;AHP 0;AHM 0;
       WS 0;WQ 0;ETA1 0;ETA2 0;ETA3 0;
       ETA4 0;F1 0;F2 0;F3 0;F4 0;F5 0;
       F6 0;F7 0;F8 0;F9 0;F10 0;F11 0;
       F12 0;F13 0;F14 0;F15 0;F16 0;
       F17 0;F18 0;F19 0;F20 0
 :FILE:SAVE:ABORt
 Function Aborts file saving.
 Syntax :FILE:SAVE:ABORt
 Example :FILE:SAVE:ABORT
 :FILE:SAVE:ACQuisition?
 Function Queries all settings related to the file saving of
       the waveform sampling data.
 Syntax :FILE:SAVE:ACQuisition?
 Example :FILE:SAVE:ACQUISITION? ->
       :FILE:SAVE:ACQUISITION:TYPE FLOAT;
       TRACE U1
 Description This command is valid only on models with the
       advanced computation function (/G6 option).

 :FILE:SAVE:ACQuisition[:EXECute]
 Function Saves the waveform sampling data to a file.
 Syntax :FILE:SAVE:ACQuisition
       [:EXECute] {<Filename>}
 Example :FILE:SAVE:ACQUISITION:
       EXECUTE “ACQ1”
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • Specify the file name without the extension.
       • This command is an overlap command.
```
### Right column
```text
 :FILE:SAVE:ACQuisition:TRACe
 Function Sets the waveform sampling data to be saved to
       a file or queries the current setting.
 Syntax :FILE:SAVE:ACQuisition:TRACe {U<x>|
       I<x>|SPEed|TORQue|MATH<x>|FFT<x>}
       :FILE:SAVE:ACQuisition:TRACe?
       <x> of U<x>, I<x> = 1 to 4 (element)
       <x> of MATH<x> = 1 to 2 (MATH)
       <x> of FFT<x> = 1 or 2 (FFT)
 Example :FILE:SAVE:ACQUISITION:TRACE U1
       :FILE:SAVE:ACQUISITION:TRACE? ->
       :FILE:SAVE:ACQUISITION:TRACE U1
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • This command is valid when the format of
        the waveform sampling data to be saved
        (:FILE:SAVE:ACQuisition:TYPE) is
        “FLOat.” When it is {BINary|ASCii}, all
        waveform sampling data of which the waveform
        display is turned ON are saved.
       • {SPEed|TORQue} are valid only on models
        with the motor evaluation function (/MTR
        option).
 :FILE:SAVE:ACQuisition:TYPE
 Function Sets the format of the waveform sampling data to
       be saved or queries the current setting.
 Syntax :FILE:SAVE:ACQuisition:
       TYPE {BINary|ASCii|FLOat}
       :FILE:SAVE:ACQuisition:TYPE?
 Example :FILE:SAVE:ACQUISITION:TYPE FLOAT
       :FILE:SAVE:ACQUISITION:TYPE? ->
       :FILE:SAVE:ACQUISITION:TYPE FLOAT
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :FILE:SAVE:ANAMing
 Function Sets whether to automatically name the files to
       be saved or queries the current setting.
 Syntax :FILE:SAVE:ANAMing {<Boolean>}
       :FILE:SAVE:ANAMing?
 Example :FILE:SAVE:ANAMING ON
       :FILE:SAVE:ANAMING? ->
       :FILE:SAVE:ANAMING 1
 :FILE:SAVE:COMMent
 Function Sets the comment to be added to the file to be
       saved or queries the current setting.
 Syntax :FILE:SAVE:COMMent {<String>}
       :FILE:SAVE:COMMent?
       <String> = Up to 25 characters
 Example :FILE:SAVE:COMMENT “CASE1”
       :FILE:SAVE:COMMENT? ->
       :FILE:SAVE:COMMENT “CASE1”
```

## Page 6-49

### Left column
```text
   :FILE:SAVE:NUMeric?
   Function Queries all settings related to the saving of
         numeric data files.
   Syntax :FILE:SAVE:NUMeric?
   Example :FILE:SAVE:NUMERIC? ->
         :FILE:SAVE:NUMERIC:TYPE ASCII;
         NORMAL:ELEMENT1 1;ELEMENT2 0;
         ELEMENT3 0;ELEMENT4 0;SIGMA 0;
         SIGMB 0;U 1;I 1;P 1;S 1;Q 1;
         LAMBDA 1;PHI 1;FU 1;FI 1;UPPEAK 0;
         UMPEAK 0;IPPEAK 0;IMPEAK 0;CFU 0;
         CFI 0;PC 0;TIME 0;WH 0;WHP 0;WHM 0;
         AH 0;AHP 0;AHM 0;WS 0;WQ 0;ETA1 0;
         ETA2 0;ETA3 0;ETA4 0;F1 0;F2 0;
         F3 0;F4 0;F5 0;F6 0;F7 0;F8 0;F9 0;
         F10 0;F11 0;F12 0;F13 0;F14 0;
         F15 0;F16 0;F17 0;F18 0;F19 0;F20 0
   :FILE:SAVE:NUMeric:CBCycle?
   Function Queries all settings related to Cycle by Cycle
         measurement items saved to numeric data files
         or queries the current setting
   Syntax :FILE:SAVE:NUMeric:CBCycle?
   Example :FILE:SAVE:NUMERIC:CBCYCLE? ->
         :FILE:SAVE:NUMERIC:CBCYCLE
         :ELEMENT1 1;ELEMENT2 0;ELEMENT3 0;
         ELEMENT4 0;SIGMA 0;SIGMB 0;FREQ 1;
         U 1;I 1;P 1;S 1;Q 1;LAMBDA 1
   :FILE:SAVE:NUMeric:CBCycle:ALL
   Function Collectively turns ON/OFF the output of all
         elements and functions when saving numeric
         data from Cycle by Cycle measurement to a file.
   Syntax :FILE:SAVE:NUMeric:CBCycle:
         ALL {<Boolean>}
   Example :FILE:SAVE:NUMERIC:CBCYCLE:ALL ON
```
### Right column
```text
                      6.8 FILE Group

 :FILE:SAVE:NUMeric:CBCycle:{ELEMent<
 x>|SIGMA|SIGMB}
 Function Turns ON/OFF the output of {each element | ΣA
       | ΣB} when saving numeric data from Cycle by
       Cycle measurement to a file.
 Syntax :FILE:SAVE:NUMeric:
       CBCycle:{ELEMent<x>|SIGMA|SIGMB}
       {<Boolean>}
       :FILE:SAVE:NUMeric:
       CBCycle:{ELEMent<x>|SIGMA|SIGMB}?
       <x> = 1 to 4
 Example :FILE:SAVE:NUMERIC:CBCYCLE:
       ELEMENT1 ON
       :FILE:SAVE:NUMERIC:CBCYCLE:
       ELEMENT1? -> :FILE:SAVE:NUMERIC:
       CBCYCLE:ELEMENT1 1
 Description • “:FILE:SAVE:NUMeric:CBCycle:SIGMA” is
        available for models with 2 elements or more.
        Also, to turn output ON, wiring unit ΣA must
        exist per the wiring system setting command
        ([:INPut]WIRing).
       • “:FILE:SAVE:NUMeric:CBCycle:SIGMB” is
        valid for models with 4 elements. Also, to turn
        output ON, wiring unit ΣB must exist per the
        wiring system setting command ([:INPut]
        WIRing).
 :FILE:SAVE:NUMeric:CBCycle:<Function>
 Function Turns ON/OFF the output of each function
       when saving numeric data from Cycle by Cycle
       measurement to a file or queries the current
       setting.
 Syntax :FILE:SAVE:NUMeric:
       CBCycle:<Function> {<Boolean>}
       :FILE:SAVE:NUMeric:
       CBCycle:<Function>?
       <Function> = {FREQ|U|I|P|S|Q|LAMBda|
       SPEed|TORQue|PM}
 Example :FILE:SAVE:NUMERIC:CBCYCLE:U ON
       :FILE:SAVE:NUMERIC:CBCYCLE:U? ->
       :FILE:SAVE:NUMERIC:CBCYCLE:U 1
 Description {SPEed|TORQue|PM} is only available on
       models with the motor evaluation function (/MTR
       option).
 :FILE:SAVE:NUMeric[:EXECute]
 Function Saves the numeric data to a file.
 Syntax :FILE:SAVE:NUMeric[:EXECute]
       {<Filename>}
 Example :FILE:SAVE:NUMERIC:EXECUTE “NUM1”
 Description • Specify the file name without the extension.
       • This command is an overlap command.
```

## Page 6-50

### Left column
```text
 6.8 FILE Group

 :FILE:SAVE:NUMeric:NORMal?
 Function Queries all settings related to the items saved to
       numeric data files.
 Syntax :FILE:SAVE:NUMeric:NORMal?
 Example :FILE:SAVE:NUMERIC:NORMAL? ->
       :FILE:SAVE:NUMERIC:NORMAL:
       ELEMENT1 1;ELEMENT2 0;ELEMENT3 0;
       ELEMENT4 0;SIGMA 0;SIGMB 0;U 1;I 1;
       P 1;S 1;Q 1;LAMBDA 1;PHI 1;FU 1;
       FI 1;UPPEAK 0;UMPEAK 0;IPPEAK 0;
       IMPEAK 0;CFU 0;CFI 0;PC 0;TIME 0;
       WH 0;WHP 0;WHM 0;AH 0;AHP 0;AHM 0;
       WS 0;WQ 0;ETA1 0;ETA2 0;ETA3 0;
       ETA4 0;F1 0;F2 0;F3 0;F4 0;F5 0;
       F6 0;F7 0;F8 0;F9 0;F10 0;F11 0;
       F12 0;F13 0;F14 0;F15 0;F16 0;
       F17 0;F18 0;F19 0;F20 0
 :FILE:SAVE:NUMeric:NORMal:ALL
 Function Collectively turns ON/OFF the output of all element
       functions when saving the numerical data file.
 Syntax :FILE:SAVE:NUMeric:NORMal:
       ALL {<Boolean>}
 Example :FILE:SAVE:NUMERIC:NORMAL:ALL ON
 :FILE:SAVE:NUMeric:NORMal:{ELEMent<x
 >|SIGMA|SIGMB}
 Function Turns ON/OFF the output of {each
       element|ΣA|ΣB} when saving the numeric data to
       file.
 Syntax :FILE:SAVE:NUMeric:NORMal:
       {ELEMent<x>|SIGMA|SIGMB} {<Boolean>}
       :FILE:SAVE:NUMeric:NORMal:
       {ELEMent<x>|SIGMA|SIGMB}?
       <x> = 1 to 4
 Example :FILE:SAVE:NUMERIC:NORMAL:
       ELEMENT1 ON
       :FILE:SAVE:NUMERIC:NORMAL:ELEMENT1?
       -> :FILE:SAVE:NUMERIC:NORMAL:
       ELEMENT1 1
 Description • :FILE:SAVE:NUMeric:NORMal:SIGMA is
        valid on models with two or more elements. To
        turn the output ON, wiring unit ΣA must exist by
        setting the wiring system beforehand using the
        [:INPut]WIRing command.
       • :FILE:SAVE:NUMeric:NORMal:SIGMB is
        valid on models with four elements. To turn
        the output ON, wiring unit ΣB must exist by
        setting the wiring system beforehand using the
        [:INPut]WIRing command.
```
### Right column
```text
 :FILE:SAVE:NUMeric:NORMal:PRESet<x>
 Function Presets the output ON/OFF pattern of the
       element function for saving the numeric data to
       file.
 Syntax :FILE:SAVE:NUMeric:NORMal:PRESet<x>
       <x> = 1 to 2 (preset pattern number)
 Example :FILE:SAVE:NUMERIC:NORMAL:PRESET1
 Description For details on the output pattern when preset is
       executed, see the User’s Manual IM WT3001E-
       01EN.
 :FILE:SAVE:NUMeric:NORMal:<Function>
 Function Turns ON/OFF the output of the function when
       saving the numerical data file or queries the
       current setting.
 Syntax :FILE:SAVE:NUMeric:NORMal:
       <Function> {<Boolean>}
       :FILE:SAVE:NUMeric:NORMal:
       <Function>?
       <Function> = {U|I|P|S|Q|...}(See the
       function selection list (1) of “DISPlay group” on
       page 6-44.)
 Example :FILE:SAVE:NUMERIC:NORMAL:U ON
       :FILE:SAVE:NUMERIC:NORMAL:U? ->
       :FILE:SAVE:NUMERIC:NORMAL:U 1
 :FILE:SAVE:NUMeric:TYPE
 Function Sets the format of the numeric data to be saved
       or queries the current setting.
 Syntax :FILE:SAVE:NUMeric:TYPE {ASCii|
       FLOat}
       :FILE:SAVE:NUMeric:TYPE?
 Example :FILE:SAVE:NUMERIC:TYPE ASCII
       :FILE:SAVE:NUMERIC:TYPE? ->
       :FILE:SAVE:NUMERIC:TYPE ASCII
 :FILE:SAVE:SETup[:EXECute]
 Function Saves of the setup parameter file.
 Syntax :FILE:SAVE:SETup[:EXECute]
       {<Filename>}
 Example :FILE:SAVE:SETUP:EXECUTE “SETUP1”
 Description • Specify the file name without the extension.
       • This command is an overlap command.

 :FILE:SAVE:WAVE?
 Function Queries all settings related to the saving of
       waveform display data files.
 Syntax :FILE:SAVE:WAVE?
 Example :FILE:SAVE:WAVE? ->
       :FILE:SAVE:WAVE:TYPE BINARY
```

## Page 6-51

### Left column
```text
   :FILE:SAVE:WAVE[:EXECute]
   Function Executes the saving of the waveform display data
         file.
   Syntax :FILE:SAVE:WAVE[:EXECute]
         {<Filename>}
   Example :FILE:SAVE:WAVE:EXECUTE “WAVE1”
   Description • Specify the file name without the extension.
         • This command is an overlap command.
   :FILE:SAVE:WAVE:TRACe
   Function Sets the waveform to be saved or queries the
         current setting.
   Syntax :FILE:SAVE:WAVE:TRACe {U<x>|I<x>|
         SPEed|TORQue|MATH<x>}
         :FILE:SAVE:WAVE:TRACe?
         <x> of U<x>, I<x> = 1 to 4 (element)
         <x> of MATH<x> = 1 to 2 (MATH)
   Example :FILE:SAVE:WAVE:TRACE U1
         :FILE:SAVE:WAVE:TRACE? ->
         :FILE:SAVE:WAVE:TRACE U1
   Description • This command is valid when the format of the
          waveform display data to be saved (:FILE:
          SAVE:WAVE:TYPE) is “FLOat.” When it is
          {BINary|ASCii}, all waveforms of which the
          display is turned ON are saved.
         • {SPEed|TORQue} are valid only on models
          with the motor evaluation function (/MTR
          option).
         • MATH<x> is valid only on models with the
          advanced computation function (/G6 option).
   :FILE:SAVE:WAVE:TYPE
   Function Sets the format of the waveform display data to
         be saved or queries the current setting.
   Syntax :FILE:SAVE:WAVE:TYPE {BINary|ASCii|
         FLOat}
         :FILE:SAVE:WAVE:TYPE?
   Example :FILE:SAVE:WAVE:TYPE BINARY
         :FILE:SAVE:WAVE:TYPE? ->
         :FILE:SAVE:WAVE:TYPE BINARY
```
### Right column
```text
                      6.8 FILE Group
```

## Page 6-52

### Section introduction
```text
   6.9    FLICker   Group

 The FLICker group contains commands related to flicker measurement.
 These commands allow you to enter and query the same settings that are available under ITEM in the Flicker Items
 menu and under FORM in the Flicker Form menu on the front panel.
 Note that the commands in this group are only available with the flicker measurement function (/FL option).
```
### Left column
```text
 :FLICker?
 Function Queries all settings related to flicker
       measurement.
 Syntax :FLICker?
 Example :FLICKER? -> :FLICKER:
       MEASUREMENT FLICKER;ELEMENT1 1;
       ELEMENT2 0;ELEMENT3 0;
       INTERVAL 10,0;COUNT 12;
       FREQUENCY 50;UN:MODE AUTO;
       VALUE 230.00;:FLICKER:DC:STATE 1;
       LIMIT 3.30;:FLICKER:DMAX:STATE 1;
       LIMIT 4.00;:FLICKER:DT:STATE 1;
       LIMIT 500,3.30;:FLICKER:PST:
       STATE 1;LIMIT 1.00;:FLICKER:PLT:
       STATE 1;LIMIT 0.65;NVALUE 12;:
       FLICKER:DMIN:LIMIT 0.10
 :FLICker:COUNt
 Function Sets the number of measurements for the short-
       term flicker value Pst or queries the current
       setting.
 Syntax :FLICker:COUNt {<NRf>}
       :FLICker:COUNt?
       <NRf> = 1 to 99 (no. of measurements)
 Example :FLICKER:COUNT 12
       :FLICKER:COUNT? ->
       :FLICKER:COUNT 12
 Description This setting is available with normal flicker
       measurement (:FLICker:MEASurement
       FLICker).
       For measurement of dmax caused by manual
       switching (:FLICker:MEASurement DMAX), the
       number of measurements is fixed at 24.
 :FLICker:DC?
 Function Sets all settings related to the relative steady-
       state voltage change dc or queries the current
       setting.
 Syntax :FLICker:DC?
 Example :FLICKER:DC? ->
       :FLICKER:DC:STATE 1;LIMIT 3.30
```
### Right column
```text
 :FLICker:DC:LIMit
 Function Sets the limit of the relative steady-state voltage
       change dc or queries the current setting.
 Syntax :FLICker:DC:LIMit {<NRf>}
       :FLICker:DC:LIMit?
       <NRf> = 1.00 to 99.99 (limit[%])
 Example :FLICKER:DC:LIMIT 3.30
       :FLICKER:DC:LIMIT? ->
       :FLICKER:DC:LIMIT 3.30
 :FLICker:DC[:STATe]
 Function Turns ON/OFF judgment of the relative steady-
       state voltage change dc or queries the current
       setting.
 Syntax :FLICker:DC[:STATe] {<Boolean>}
       :FLICker:DC:STATe?
 Example :FLICKER:DC:STATE ON
       :FLICKER:DC:STATE? ->
       :FLICKER:DC:STATE 1

 :FLICker:DISPlay?
 Function Queries all settings related to flicker measurement
       display.
 Syntax :FLICker:DISPlay?
 Example :FLICKER:DISPLAY? ->
       :FLICKER:DISPLAY:ELEMENT 1;PERIOD 1
 :FLICker:DISPlay:ELEMent
 Function Sets the element to be displayed for flicker
       measurement display or queries the current
       setting.
 Syntax :FLICker:DISPlay:ELEMent {<NRf>}
       :FLICker:DISPlay:ELEMent?
       <NRf> = 1 to 4 (element)
 Example :FLICKER:DISPLAY:ELEMENT 1
       :FLICKER:DISPLAY:ELEMENT? ->
       :FLICKER:DISPLAY:ELEMENT 1
 Description You can make the same setting or query with the
       “:DISPlay:FLICker:ELEMent” command.
```

## Page 6-53

### Left column
```text
   :FLICker:DISPlay:PAGE
   Function Sets the page numbers to be displayed for flicker
         measurement display or queries the current
         setting.
   Syntax :FLICker:DISPlay:PAGE {<NRf>}
         :FLICker:DISPlay:PAGE?
         <NRf> = 1 to 9 (page number)
   Example :FLICKER:DISPLAY:PAGE 1
         :FLICKER:DISPLAY:PAGE? ->
         :FLICKER:DISPLAY:PAGE 1
   Description You can make the same setting or query with the
         “:DISPlay:FLICker:PAGE” command.
   :FLICker:DISPlay:PERiod
   Function Sets the display observation period number
         for flicker measurement display or queries the
         current setting.
   Syntax :FLICker:DISPlay:PERiod {<NRf>}
         :FLICker:DISPlay:PERiod?
         <NRf> = 1 to 99 (observation period number)
   Example :FLICKER:DISPLAY:PERIOD 1
         :FLICKER:DISPLAY:PERIOD? ->
         :FLICKER:DISPLAY:PERIOD 1
   Description You can make the same setting or query with the
         “:DISPlay:FLICker:PERiod” command.
   :FLICker:DMAX?
   Function Sets all settings related to the maximum relative
         voltage change dmax or queries the current
         setting.
   Syntax :FLICker:DMAX?
   Example :FLICKER:DMAX? ->
         :FLICKER:DMAX:STATE 1;LIMIT 4.00
   :FLICker:DMAX:LIMit
   Function Sets the limit of the maximum relative voltage
         change dmax or queries the current setting.
   Syntax :FLICker:DMAX:LIMit {<NRf>}
         :FLICker:DMAX:LIMit?
         <NRf> = 1.00 to 99.99 (limit[%])
   Example :FLICKER:DMAX:LIMIT 4.00
         :FLICKER:DMAX:LIMIT? ->
         :FLICKER:DMAX:LIMIT 4.00

   :FLICker:DMAX[:STATe]
   Function Turns ON/OFF judgment of the maximum relative
         voltage change dmax or queries the current
         setting.
   Syntax :FLICker:DMAX[:STATe] {<Boolean>}
         :FLICker:DMAX:STATe?
   Example :FLICKER:DMAX:STATE ON
         :FLICKER:DMAX:STATE? ->
         :FLICKER:DMAX:STATE 1
```
### Right column
```text
                    6.9 FLICker Group

 :FLICker:DMIN?
 Function Sets all settings related to the steady-state range
       dmin or queries the current setting.
 Syntax :FLICker:DMIN?
 Example :FLICKER:DMIN? ->
       :FLICKER:DMIN:LIMIT 0.10

 :FLICker:DMIN:LIMit
 Function Sets the limit of the steady-state range dmin or
       queries the current setting.
 Syntax :FLICker:DMIN:LIMit {<NRf>}
       :FLICker:DMIN:LIMit?
       <NRf> = 0.10.00 to 9.99 (limit[%])
 Example :FLICKER:DMIN:LIMIT 0.10
       :FLICKER:DMIN:LIMIT? ->
       :FLICKER:DMIN:LIMIT 0.10
 :FLICker:DT?
 Function Sets all settings related to the relative voltage
       change time d(t) or queries the current setting.
 Syntax :FLICker:DT?
 Example :FLICKER:DT? ->
       :FLICKER:DT:STATE 1;LIMIT 500,3.30
 :FLICker:DT:LIMit
 Function Sets the limit of the relative voltage change time
       d(t) or queries the current setting.
 Syntax :FLICker:DT:LIMit {<NRf>[,<NRf>]}
       :FLICker:DT:LIMit?
       1st <NRf> = 1 to 99999 (limit[ms])
       2nd <NRf> = 1.00 to 99.99 (threshold level[%])
 Example :FLICKER:DT:LIMIT 500,3.30
       :FLICKER:DT:LIMIT? ->
       :FLICKER:DT:LIMIT 500,3.30
 Description If the second parameter (threshold level) is not to
       be set, it can be omitted.
 :FLICker:DT[:STATe]
 Function Turns ON/OFF judgment of the relative voltage
       change time d(t) or queries the current setting.
 Syntax :FLICker:DT[:STATe] {<Boolean>}
       :FLICker:DT:STATe?
 Example :FLICKER:DT:STATE ON
       :FLICKER:DT:STATE? ->
       :FLICKER:DT:STATE 1
```

## Page 6-54

### Left column
```text
 6.9 FLICker Group

 :FLICker:EDITion
 Function Sets the IEC standard edition for flicker
       measurement or queries the current setting.
 Syntax :FLICker:EDITion {<Edition>}
       :FLICker:EDITion?
       <Edition> = {ED2P0|ED1P1}
 Example :FLICKER:EDITION ED2P0
       :FLICKER:EDITION? ->
       :FLICKER:EDITION ED2P0
 Description ED2P0: IEC61000-4-15 Ed2.0
       ED1P1: IEC61000-4-15 Ed1.1
 :FLICker:ELEMent<x>
 Function Sets the target element flicker measurement or
       queries the current setting.
 Syntax :FLICker:ELEMent<x> {<Boolean>}
       :FLICker:ELEMent<x>?
       <x> = 1 to 4 (element)
 Example :FLICKER:ELEMENT1 ON
       :FLICKER:ELEMENT1? ->
       :FLICKER:ELEMENT1 1
 Description When turned ON (1), that element is targeted for
       flicker measurement.
 :FLICker:FREQuency
 Function Sets the target frequency for flicker measurement
       or queries the current setting.
 Syntax :FLICker:FREQuency {<NRf>}
       :FLICker:FREQuency?
       <NRf> = 50, 60 (target frequency [Hz])
 Example :FLICKER:FREQUENCY 50
       :FLICKER:FREQUENCY? ->
       :FLICKER:FREQUENCY 50
 :FLICker:INITialize
 Function Initializes flicker measurement.
 Syntax :FLICker:INITialize
 Example :FLICKER:INITIALIZE
```
### Right column
```text
 :FLICker:INTerval
 Function Sets the time per measurement of the short-term
       flicker value Pst or queries the current setting.
 Syntax :FLICker:INTerval {<NRf>,<NRf>}
       :FLICker:INTerval?
       <NRf>,<NRf> = 0,30 to 15,00 (measurement
       time: minutes, seconds)
 Example :FLICKER:INTERVAL 10,00
       :FLICKER:INTERVAL? ->
       :FLICKER:INTERVAL 10,00
 Description • This setting is available with normal flicker
        measurement (:FLICker:MEASurement
        FLICker). The time per measurement
        of dmax caused by manual switching
        (:FLICker:MEASurement DMAX) is fixed at
        1 (min) 00 (sec).
       • The setting resolution for the measurement
        time is 2 seconds. When an odd number of
        seconds is set, it is rounded up to the next
        second.
 :FLICker:JUDGe
 Function Finishes measurement of dmax caused by
       manual switching and performs judgment.
 Syntax :FLICker:JUDGe
 Example :FLICKER:JUDGE
 Description This command can be executed with
       measurement of dmax caused by manual
       switching (:FLICker:MEASurement DMAX).
       An error occurs if used during normal flicker
       measurement (:FLICker:MEASurement
       FLICker).
 :FLICker:MEASurement
 Function Sets the flicker measurement method or queries
       the current setting.
 Syntax :FLICker:MEASurement {FLICker|DMAX}
       :FLICker:MEASurement?
       FLICker = Normal flicker measurement
       DMAX = measurement of dmax caused by
       manual switching
 Example :FLICKER:MEASUREMENT FLICKER
       :FLICKER:MEASUREMENT? ->
       :FLICKER:MEASUREMENT FLICKER
```

## Page 6-55

### Left column
```text
   :FLICker:MOVe
   Function Moves the observation period number for
         measurement of dmax caused by manual
         switching.
   Syntax :FLICker:MOVe {<NRf>}
         <NRf> = 1 to 24 (observation period number of
         destination)
   Example :FLICKER:MOVE 1
   Description • The command re-executes measurement if
          dmax measurement of certain observation
          periods is not made correctly.
         • This command can be executed with
          measurement of dmax caused by manual
          switching (:FLICker:MEASurement DMAX).
          An error occurs if used during normal flicker
          measurement (:FLICker:MEASurement
          FLICker).
   :FLICker:PLT?
   Function Queries all settings related to the long-term flicker
         value Plt.
   Syntax :FLICker:PLT?
   Example :FLICKER:PLT? -> :FLICKER:PLT:
         STATE 1;LIMIT 0.65;NVALUE 12
   :FLICker:PLT:LIMit
   Function Sets the limit of the long-term flicker value Plt or
         queries the current setting.
   Syntax :FLICker:PLT:LIMit {<NRf>}
         :FLICker:PLT:LIMit?
         <NRf> = 0.10 to 99.99 (limit)
   Example :FLICKER:PLT:LIMIT 0.65
         :FLICKER:PLT:LIMIT? ->
         :FLICKER:PLT:LIMIT 0.65
   :FLICker:PLT:NVALue
   Function Sets constant N for the equation used to compute
         the long-term flicker value Plt or queries the
         current setting.
   Syntax :FLICker:PLT:NVALue {<NRf>}
         :FLICker:PLT:NVALue?
         <NRf> = 1 to 99 (constant N)
   Example :FLICKER:PLT:NVALUE 12
         :FLICKER:PLT:NVALUE? ->
         :FLICKER:PLT:NVALUE 12

   :FLICker:PLT[:STATe]
   Function Turns ON/OFF judgment of the long-term flicker
         value Plt or queries the current setting.
   Syntax :FLICker:PLT[:STATe] {<Boolean>}
         :FLICker:PLT:STATe?
   Example :FLICKER:PLT:STATE ON
         :FLICKER:PLT:STATE? ->
         :FLICKER:PLT:STATE 1
```
### Right column
```text
                    6.9 FLICker Group

 :FLICker:PST?
 Function Queries all settings related to the short-term
       flicker value Pst.
 Syntax :FLICker:PST?
 Example :FLICKER:PST? ->
       :FLICKER:PST:STATE 1;LIMIT 1.00

 :FLICker:PST:LIMit
 Function Sets the limit for the short-term flicker value or
       queries the current setting.
 Syntax :FLICker:PST:LIMit {<NRf>}
       :FLICker:PST:LIMit?
       <NRf> = 0.10 to 99.99 (limit)
 Example :FLICKER:PST:LIMIT 1.00
       :FLICKER:PST:LIMIT? ->
       :FLICKER:PST:LIMIT 1.00
 :FLICker:PST[:STATe]
 Function Turns ON/OFF judgment of the short-term flicker
       value Pst or queries the current setting.
 Syntax :FLICker:PST[:STATe] {<Boolean>}
       :FLICker:PST:STATe?
 Example :FLICKER:PST:STATE ON
       :FLICKER:PST:STATE? ->
       :FLICKER:PST:STATE 1
 :FLICker:P3D3
 Function Sets the edition of IEC 61000-3-3 or queries the
       current setting.
 Syntax :FLICker:P3D3 {<Edition>}
       :FLICker:P3D3?
       <Edition> = {ED3P0|ED2P0}
       ED3P0:IEC61000-3-3 Ed 3.0
       ED2P0:IEC61000-3-3 Ed 2.0
 Example :FLICKER:P3D3 ED3P0
       :FLICKER:P3D3 ? ->
       :FLICKER:P3D3 ED3P0
 :FLICker:P4D15
 Function Sets the edition of IEC 61000-4-15 or queries the
       current setting.
 Syntax :FLICker:P4D15 {<Edition>}
       :FLICker:P4D15?
       <Edition> = {ED2P0|ED1P1}
       ED2P0:IEC61000-4-15 Ed2.0
       ED1P1:IEC61000-4-15 Ed1.1
 Example :FLICKER: P4D15 ED2P0
       :FLICKER:P4D15 ? ->
       :FLICKER:P4D15 ED2P0
 Description This is the same setting or query as with the
       “:FLICker:EDITion” command.
 :FLICker:RESet
 Function Resets measured flicker data.
 Syntax :FLICker:RESet
 Example :FLICKER:RESET
```

## Page 6-56

### Left column
```text
 6.9 FLICker Group

 :FLICker:STARt
 Function Starts flicker measurement.
 Syntax :FLICker:STARt
 Example :FLICKER:START

 :FLICker:STATe?
 Function Queries the status of flicker measurement.
 Syntax :FLICker:STATe?
 Example :FLICKER:STATE? -> RESET
 Description The contents of the response are as follows:
           RESet = Reset status
           INITialize = Initializing
           READy = Measurement start wait state
           STARt = Measuring
           COMPlete = Measurement stopped,
                 judgment results displayed
 :FLICker:TMAX?
 Function Queries all settings related to Tmax.
 Syntax :FLICker:TMAX?
 Example :FLICKER:TMAX? ->
       :FLICKER:TMAX:STATE 1;LIMIT 500,3.30
 Description This is the same query as with the
       “:FLICker:DT?” command.
 :FLICker:TMAX:LIMit
 Function Sets the limit of the Tmax or queries the current
       setting.
 Syntax :FLICker:TMAX:LIMit {<NRf>:LIMit
       {<NRf>[,<NRf>]}
       :FLICker:TMAX:LIMit?
       1st <NRf> = 1 to 99999 (limit [ms])
       2nd <NRf> = 1.00 to 99.99 (threshold level [%])
 Example :FLICKER:TMAX:LIMIT 500,3.30
       :FLICKER:TMAX:LIMIT? ->
       :FLICKER:TMAX:LIMIT 500,3.30
 Description This is the same setting or query as with the
       “:FLICker:DT:LIMit” command.
 :FLICker:TMAX[:STATe]
 Function Turns ON/OFF judgment of the Tmax or queries
       the current setting.
 Syntax :FLICker:TMAX[:STATe] {<Boolean>}
       :FLICker:TMAX:STATe?
 Example :FLICKER:TMAX:STATE ON
       :FLICKER:TMAX:STATE? ->
       :FLICKER:TMAX:STATE 1
 Description This is the same setting or query as with the
       “:FLICker:DT[:STATe]” command.
 :FLICker:UN?
 Function Queries all settings related to rated voltage Un.
 Syntax :FLICker:UN?
 Example :FLICKER:UN? -> :FLICKER:UN:
       MODE AUTO;VALUE 230.00
```
### Right column
```text
 :FLICker:UN:MODE
 Function Sets the assignment method for rated voltage Un
       or queries the current setting.
 Syntax :FLICker:UN:MODE {AUTO|SET}
       :FLICker:UN:MODE?
       AUTO = Use the voltage value measured upon
       start of measurement.
       SET = Use the predefined value
       (:FLICker:UN:VALue).
 Example :FLICKER:UN:MODE AUTO
       :FLICKER:UN:MODE? ->
       :FLICKER:UN:MODE AUTO
 :FLICker:UN:VALue
 Function Sets the predefined value of rated voltage Un or
       queries the current setting.
 Syntax :FLICker:UN:VALue {<NRf>}
       :FLICker:UN:VALue?
       <NRf> = 0.01 to 999.99 (predefined value[V])
 Example :FLICKER:UN:VALUE 230.00
       :FLICKER:UN:VALUE? ->
       :FLICKER:UN:VALUE 230.00
 :FLICker:VOLTage
 Function Sets the flicker target voltage or queries the
       current setting.
 Syntax :FLICker:VOLTage {<NRf>}
       :FLICker:VOLTage?
       <NRf> = 120, 230 (target voltage[V])
 Example :FLICKER:VOLTAGE 230
       :FLICKER:VOLTAGE? ->
       :FLICKER:VOLTAGE 230
```

## Page 6-57

### Section introduction
```text
     6.10   HARMonics      Group

   The commands in this group deal with harmonic measurement.
   You can make the same settings and inquiries as when the HRM SET on the front panel is used.
   However, the commands in this group are valid only when the advanced computation function (/G6 option) is installed.
```
### Left column
```text
   :HARMonics?
   Function Queries all settings related to harmonic
         measurement.
   Syntax :HARMonics?
   Example HARMONICS? -> :HARMONICS:
         FBAND NORMAL;PLLSOURCE U1;
         ORDER 1,100;THD TOTAL;IEC:
         OBJECT ELEMENT1;UGROUPING OFF;
         IGROUPING OFF;:HARMONICS:
         PLLWARNING:STATE 1
   :HARMonics:FBANd
   Function Sets the frequency bandwidth of the harmonic
         measurement or queries the current setting.
   Syntax :HARMonics:FBANd {NORMal|WIDE}
         :HARMonics:FBANd?
   Example :HARMONICS:FBAND NORMAL
         :HARMONICS:FBAND? ->
         :HARMONICS:FBAND NORMAL
   Description • This command is valid only on models with the
          advanced computation function (/G6 option).
         • For details on the frequency bandwidth
          corresponding to {NORMal|WIDE}, see the
          Expansion Function User’s Manual
          IM WT3001E-51EN.
   :HARMonics:IEC?
   Function Queries all settings related to IEC harmonic
         measurement.
   Syntax :HARMonics:IEC?
   Example :HARMONICS:IEC? -> :HARMONICS:IEC:
         OBJECT ELEMENT1;UGROUPING OFF;
         IGROUPING OFF
   Description This command is valid only on models with the
         advanced computation function (/G6 option).
```
### Right column
```text
 :HARMonics:IEC:OBJect
 Function Sets the IEC harmonic measurement target or
       queries the current setting.
 Syntax :HARMonics:IEC:OBJect {ELEMent<x>|
       SIGMA|SIGMB}
       :HARMonics:IEC:OBJect?
       <x> = 1 to 4 (element)
 Example :HARMONICS:IEC:OBJECT ELEMENT1
       :HARMONICS:IEC:OBJECT? ->
       :HARMONICS:IEC:OBJECT ELEMENT1
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :HARMonics:IEC:{UGRouping|IGRouping}
 Function Sets the {voltage|current} grouping of the IEC
       harmonic measurement or queries the current
       setting.
 Syntax :HARMonics:IEC:{UGRouping|
       IGRouping} {OFF|TYPE1|TYPE2}
       :HARMonics:IEC:{UGRouping|
       IGRouping}?
 Example :HARMONICS:IEC:UGROUPING OFF
       :HARMONICS:IEC:UGROUPING? ->
       :HARMONICS:IEC:UGROUPING OFF
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • For details on the grouping corresponding to
        {OFF|TYPE1|TYPE2}, see the Expansion
        Function User’s Manual IM WT3001E-51EN.
 :HARMonics:ORDer
 Function Sets the maximum and minimum orders to be
       measured or queries the current setting.
 Syntax :HARMonics:ORDer {<NRf>,<NRf>}
       :HARMonics:ORDer?
       1st <NRf> = 0 or 1 (minimum order to be
       measured)
       2nd <NRf> = 1 to 100 (maximum order to be
       measured)
 Example :HARMONICS:ORDER 1,100
       :HARMONICS:ORDER? -> :HARMONICS:ORDER
       1,100
```

## Page 6-58

### Left column
```text
 6.10 HARMonics Group

 :HARMonics:PLLSource
 Function Sets the PLL source or queries the current
       setting.
 Syntax :HARMonics:PLLSource {U<x>|I<x>|
       EXTernal|SAMPle}
       :HARMonics:PLLSource?
       <x> = 1 to 4 (element)
       EXTernal = External clock input (Ext Clk)
       SAMPle = Sampling clock input (Smp Clk)
 Example :HARMONICS:PLLSOURCE U1
       :HARMONICS:PLLSOURCE? ->
       :HARMONICS:PLLSOURCE U1
 Description • “SAMPle” is selectable only on models with the
        advanced computation function (/G6 option).
       • If SAMPle is selected, it is used in wide
        bandwidth harmonic measurement mode. In
        other measurement modes, EXTernal is used.
        “EXTernal” is also returned in response to a
        query.
 :HARMonics:PLLWarning?
 Function Queries all settings related to the warning
       messages of the PLL source.
 Syntax :HARMonics:PLLWarning?
 Example :HARMONICS:PLLWARNING? ->
       :HARMONICS:PLLWARNING:STATE 1
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :HARMonics:PLLWarning[:STATe]
 Function Sets whether to generate a warning message
       when the PLL source is not applied or queries the
       current setting.
 Syntax :HARMonics:PLLWarning
       [:STATe] {<Boolean>}
       :HARMonics:PLLWarning:STATe?
 Example :HARMONICS:PLLWARNING:STATE ON
       :HARMONICS:PLLWARNING:STATE? ->
       :HARMONICS:PLLWARNING:STATE 1
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • This setting is valid only in wide bandwidth
        harmonic measurement mode.
 :HARMonics:THD
 Function Sets the equation used to calculate the THD (total
       harmonic distortion) or queries the current setting.
 Syntax :HARMonics:THD {TOTal|FUNDamental}
       :HARMonics:THD?
 Example :HARMONICS:THD TOTAL
       :HARMONICS:THD? ->
       :HARMONICS:THD TOTAL
```

## Page 6-59

### Section introduction
```text
     6.11   HCOPy    Group

   The commands in this group deal with printing to the built-in printer or network printer.
   You can make the same settings and inquiries as when PRINT and MENU (SHIFT+PRINT) on the front panel is used.
   However, the commands in this group are valid only when the built-in printer (/B5 option) or Ethernet interface (/C7
   option) is installed.
```
### Left column
```text
   :HCOPy? (Hard COPY)
   Function Queries all settings related to the printing.
   Syntax :HCOPy?
   Example :HCOPY? -> :HCOPY:
         DIRECTION PRINTER;PRINTER:
         FORMAT HCOPY;:HCOPY:AUTO:STATE 0;:
         HCOPY:COMMENT “THIS IS TEST.”

   :HCOPy:ABORt
   Function Aborts printing or paper feeding.
   Syntax :HCOPy:ABORt
   Example :HCOPY:ABORT
   :HCOPy:AUTO?
   Function Queries all settings related to the auto print.
   Syntax :HCOPy:AUTO?
   Example :HCOPY:AUTO? -> :HCOPY:AUTO:
         STATE 1;SYNCHRONIZE TIMER;
         START 2005,1,1,0,0,0;
         END 2005,1,1,1,0,0;INTERVAL 0,0,10

   :HCOPy:AUTO:INTerval
   Function Sets the auto print interval or queries the current
         setting.
   Syntax :HCOPy:AUTO:INTerval
         {<NRf>,<NRf>,<NRf>}
         :HCOPy:AUTO:INTerval?
         {<NRf>, <NRf>, <NRf>} = 0, 0, 10 to 99, 59, 59
         1st <NRf> = 0 to 99 (hour)
         2nd <NRf> = 0 to 59 (minute)
         3rd <NRf> = 0 to 59 (second)
   Example :HCOPY:AUTO:INTERVAL 0,0,10
         :HCOPY:AUTO:INTERVAL? ->
         :HCOPY:AUTO:INTERVAL 0,0,10
```
### Right column
```text
 :HCOPy:AUTO:{STARt|END}
 Function Sets the {start|stop} reservation time of the auto
       print or queries the current setting.
 Syntax :HCOPy:AUTO:{STARt|END}
       {<NRf>,<NRf>,<NRf>,<NRf>,<NRf>,
       <NRf>}
       :HCOPy:AUTO:{STARt|END}?
       {<NRf>, <NRf>, <NRf>, <NRf>, <NRf>, <NRf>} =
       2001, 1, 1, 0, 0, 0 to 2099, 12, 31, 23, 59, 59
       1st <NRf> = 2001 to 2099 (year)
       2nd <NRf> = 1 to 12 (month)
       3rd <NRf> = 1 to 31 (day)
       4th <NRf> = 0 to 23 (hour)
       5th <NRf> = 0 to 59 (minute)
       6th <NRf> = 0 to 59 (second)
 Example :HCOPY:AUTO:START 2005,1,1,0,0,0
       :HCOPY:AUTO:START? ->
       :HCOPY:AUTO:START 2005,1,1,0,0,0
 Description This setting is valid when the synchronization
       mode (:HCOPy:AUTO:SYNChronize) is set to
       TIMer (timer synchronized printing).
 :HCOPy:AUTO[:STATe]
 Function Turns ON/OFF the auto print or queries the
       current setting.
 Syntax :HCOPy:AUTO[:STATe] {<Boolean>}
       :HCOPy:AUTO:STATe?
 Example :HCOPY:AUTO:STATE ON
       :HCOPY:AUTO:STATE? ->
       :HCOPY:AUTO:STATE 1
 :HCOPy:AUTO:SYNChronize
 Function Sets the synchronization mode of the auto print
       or queries the current setting.
 Syntax :HCOPy:AUTO:SYNChronize {TIMer|
       INTEGrate}
       :HCOPy:AUTO:SYNChronize?
       TIMer = Timer synchronized printing
       INTEGrate = Integration synchronized printing
 Example :HCOPY:AUTO:SYNCHRONIZE TIMER
       :HCOPY:AUTO:SYNCHRONIZE? ->
       :HCOPY:AUTO:SYNCHRONIZE TIMER
```

## Page 6-60

### Left column
```text
 6.11 HCOPy Group

 :HCOPy:COMMent
 Function Sets the comment displayed at the bottom of the
       screen or queries the current setting.
 Syntax :HCOPy:COMMent {<String>}
       :HCOPy:COMMent?
       <String > = 25 characters or less (However, only
       the first 20 characters are displayed.)
 Example :HCOPY:COMMENT “THIS IS TEST.”
       :HCOPY:COMMENT? -> :HCOPY:COMMENT
       “THIS IS TEST.”
 :HCOPy:DIRection
 Function Sets the printer or queries the current setting.
 Syntax :HCOPy:DIRection {PRINter|NETPrint}
       :HCOPy:DIRection?
       PRINter = Built-in printer
       NETPrint = Network printer
 Example :HCOPY:DIRECTION PRINTER
       :HCOPY:DIRECTION? -> :HCOPY:DIRECTION
       PRINTER
 Description • PRINTer is valid only when the built-in printer
        (/B5 option) is installed.
       • NETPrint is valid only when the Ethernet
        interface (/C7 option) is installed.
 :HCOPy:EXECute
 Function Executes printing.
 Syntax :HCOPy:EXECute
 Example :HCOPY:EXECUTE
 Description This command is an overlap command.

 :HCOPy:NETPrint?
 Function Queries all settings related to the printing on the
       network printer.
 Syntax :HCOPy:NETPrint?
 Example :HCOPY:NETPRINT? -> :HCOPY:
       NETPRINT:FORMAT BJ,180;COLOR 0
 Description This command is valid only on models with the
       Ethernet interface (/C7 option).
 :HCOPy:NETPrint:COLor
 Function Turns ON/OFF color printing on the network
       printer or queries the current setting.
 Syntax :HCOPy:NETPrint:COLor {<Boolean>}
       :HCOPy:NETPrint:COLor?
 Example :HCOPY:NETPRINT:COLOR OFF
       :HCOPY:NETPRINT:COLOR? ->
       :HCOPY:NETPRINT:COLOR 0
 Description This command is valid only on models with the
       Ethernet interface (/C7 option).
```
### Right column
```text
 :HCOPy:NETPrint:FORMat
 Function Sets the printer description language for printing
       on a network printer or queries the current setting.
 Syntax :HCOPy:NETPrint:FORMat {PCL5|LIPS3|
       BJ,<NRf>}
       :HCOPy:NETPrint:FORMat?
       <NRf> = 180, 300, or 360 (dpi, resolution)
 Example :HCOPY:NETPRINT:FORMAT BJ,180
       :HCOPY:NETPRINT:FORMAT? ->
       :HCOPY:NETPRINT:FORMAT BJ,180
 Description • Set <NRf> only when BJ is selected.
       • This command is valid only on models with the
        Ethernet interface (/C7 option).
 :HCOPy:PRINter?
 Function Queries all settings related to printing on the built-
       in printer.
 Syntax :HCOPy:PRINter?
 Example :HCOPY:PRINTER? ->
       :HCOPY:PRINTER:FORMAT HCOPY
 Description This command is valid only when the built-in
       printer (/B5 option) is installed.
 :HCOPy:PRINter:FEED
 Function Executes paper feeding of the built-in printer.
 Syntax :HCOPy:PRINter:FEED
 Example :HCOPY:PRINTER FEED
 Description • This command is valid only when the built-in
        printer (/B5 option) is installed.
       • This command is an overlap command.

 :HCOPy:PRINter:FORMat
 Function Sets the contents to be printed on the built-in
       printer or queries the current setting.
 Syntax :HCOPy:PRINter:FORMat {HCOPy|LIST}
       :HCOPy:PRINter:FORMat?
       HCOPy = Screen image data
       LIST = Numeric data list
 Example :HCOPY:PRINTER:FORMAT HCOPY
       :HCOPY:PRINTER:FORMAT? ->
       :HCOPY:PRINTER:FORMAT HCOPY
 Description This command is valid only when the built-in
       printer (/B5 option) is installed.
```

## Page 6-61

### Left column
```text
   :HCOPy:PRINter:LIST?
   Function Queries all settings related to the printing of the
         numeric data list on the built-in printer.
   Syntax :HCOPy:PRINter:LIST?
   Example :HCOPY:PRINTER:LIST? -> :HCOPY:
         PRINTER:LIST:INFORMATION 1;NORMAL:
         ELEMENT1 1;ELEMENT2 0;ELEMENT3 0;
         ELEMENT4 0;SIGMA 0;SIGMB 0;U 1;I 1;
         P 1;S 1;Q 1;LAMBDA 1;PHI 1;FU 1;
         FI 1;UPPEAK 0;UMPEAK 0;IPPEAK 0;
         IMPEAK 0;CFU 0;CFI 0;PC 0;TIME 0;
         WH 0;WHP 0;WHM 0;AH 0;AHP 0;AHM 0;
         WS 0;WQ 0;ETA1 0;ETA2 0;ETA3 0;
         ETA4 0;F1 0;F2 0;F3 0;F4 0;F5 0;
         F6 0;F7 0;F8 0;F9 0;F10 0;F11 0;
         F12 0;F13 0;F14 0;F15 0;F16 0;
         F17 0;F18 0;F19 0;F20 0
   Description This command is valid only when the built-in
         printer (/B5 option) is installed.
   :HCOPy:PRINter:LIST:INFOrmation
   Function Sets whether to add setup parameters when
         printing the numeric data list on the built-in printer
         or queries the current setting.
   Syntax :HCOPy:PRINter:LIST:INFOrmation
         {<Boolean>}
         :HCOPy:PRINter:LIST:INFOrmation?
   Example :HCOPY:PRINTER:LIST:INFORMATION ON
         :HCOPY:PRINTER:LIST:INFORMATION? ->
         :HCOPY:PRINTER:LIST:INFORMATION 1
   Description This command is valid only when the built-in
         printer (/B5 option) is installed.
   :HCOPy:PRINter:LIST:NORMal?
   Function Queries all settings related to the printed items of
         the numeric data list using the built-in printer.
   Syntax :HCOPy:PRINter:LIST:NORMal?
   Example :HCOPY:PRINTER:LIST:NORMAL? ->
         :HCOPY:PRINTER:LIST:NORMAL:
         ELEMENT1 1;ELEMENT2 0;ELEMENT3 0;
         ELEMENT4 0;SIGMA 0;SIGMB 0;U 1;I 1;
         P 1;S 1;Q 1;LAMBDA 1;PHI 1;FU 1;
         FI 1;UPPEAK0;UMPEAK 0;IPPEAK 0;
         IMPEAK 0;CFU 0;CFI 0;PC 0;TIME 0;
         WH 0;WHP 0;WHM 0;AH 0;AHP 0;AHM 0;
         WS 0;WQ 0;ETA1 0;ETA2 0;ETA3 0;
         ETA4 0;F1 0;F2 0;F3 0;F4 0;F5 0;
         F6 0;F7 0;F8 0;F9 0;F10 0;F11 0;
         F12 0;F13 0;F14 0;F15 0;F16 0;
         F17 0;F18 0;F19 0;F20 0
   Description This command is valid only when the built-in
         printer (/B5 option) is installed.
```
### Right column
```text
                    6.11 HCOPy Group

 :HCOPy:PRINter:LIST[:NORMal]:ALL
 Function Collectively turns ON/OFF the output of all
       element functions when printing the numeric data
       list on the built-in printer.
 Syntax :HCOPy:PRINter:LIST[:NORMal]:
       ALL {<Boolean>}
 Example :HCOPY:PRINTER:LIST:NORMAL:ALL ON
 Description This command is valid only when the built-in
       printer (/B5 option) is installed.
 :HCOPy:PRINter:LIST[:NORMal]:{ELEMen
 t<x>|SIGMA|SIGMB}
 Function Turns ON/OFF the output of {each
       element|ΣA|ΣB} when printing the numeric data
       list on the built-in printer.
 Syntax :HCOPy:PRINter:LIST[:NORMal]:
       {ELEMent<x>|SIGMA|SIGMB} {<Boolean>}
       :HCOPy:PRINter:LIST[:NORMal]:
       {ELEMent<x>|SIGMA|SIGMB}?
       <x> = 1 to 4
 Example :HCOPY:PRINTER:LIST:NORMAL:
       ELEMENT1 ON
       :HCOPY:PRINTER:LIST:NORMAL:
       ELEMENT1? -> :HCOPY:PRINTER:LIST:
       NORMAL:ELEMENT1 1
 Description • This command is valid only when the built-in
        printer (/B5 option) is installed.
       • :HCOPy:PRINter:LIST[:NORMal]:
        SIGMA is valid on models with two or more
        elements. To turn the output ON, wiring unit
        ΣA must exist by setting the wiring system
        beforehand using the [:INPut]WIRing
        command.
       • :HCOPy:PRINter:LIST[:NORMal]:
        SIGMB is valid on models with four elements.
        To turn the output ON, wiring unit ΣB must exist
        by setting the wiring system beforehand using
        the [:INPut]WIRing command.
 :HCOPy:PRINter:LIST[:NORMal]:PRESet
 <x>
 Function Presets the output ON/OFF pattern of the
       element functions when printing the numeric data
       list on the built-in printer.
 Syntax :HCOPy:PRINter:LIST[:NORMal]:
       PRESet<x>
       <x> = 1 to 2 (preset pattern number)
 Example :HCOPY:PRINTER:LIST:NORMAL:PRESET1
 Description • This command is valid only when the built-in
        printer (/B5 option) is installed.
       • For details on the print pattern when preset is
        executed, see the Expansion Function User’s
        Manual IM WT3001E-51EN.
```

## Page 6-62

### Left column
```text
 6.11 HCOPy Group

 :HCOPy:PRINter:LIST[:NORMal]:<Function>
 Function urns ON/OFF the output of the function when
       printing the numerical data list using the built-in
       printer or queries the current setting.
 Syntax :HCOPy:PRINter:LIST[:NORMal]:
       <Function> {<Boolean>}
       :HCOPy:PRINter:LIST[:NORMal]:
       <Function>?
       <Function> = {U|I|P|S|Q|...}(See the
       function selection list (1) of “DISPlay group” on
       page 6-44.)
 Example :HCOPY:PRINTER:LIST:NORMAL:U ON
       :HCOPY:PRINTER:LIST:NORMAL:U? ->
       :HCOPY:PRINTER:LIST:NORMAL:U 1
 Description This command is valid only when the built-in
       printer (/B5 option) is installed.
```

## Page 6-63

### Section introduction
```text
     6.12   HOLD    Group

   The commands in this group deal with the hold function of output data.
   You can make the same settings and inquiries as when HOLD on the front panel is used.
```
### Left column
```text
   :HOLD
   Function Sets the output data (display, communications,
         etc.) hold or queries the current setting.
   Syntax :HOLD {<Boolean>}
         :HOLD?
   Example :HOLD OFF
         :HOLD? -> :HOLD 0
```

## Page 6-64

### Section introduction
```text
   6.13   IMAGe    Group

 The commands in this group deal with the saving of screen image data.
 You can make the same settings and inquiries as when IMAGE SAVE and MENU (SHIFT+ IMAGE SAVE) on the front
 panel is used.
```
### Left column
```text
 :IMAGe?
 Function Queries all settings related to the saving of
       screen image data.
 Syntax :IMAGe?
 Example :IMAGE? -> :IMAGE:FORMAT TIFF;
       COLOR OFF;COMMENT “THIS IS TEST.”;
       SAVE:ANAMING 1;NAME “”
 :IMAGe:ABORt
 Function Aborts the saving of the screen image data.
 Syntax :IMAGe:ABORt
 Example :IMAGE:ABORT

 :IMAGe:COLor
 Function Sets the color tone of the screen image data to
       be saved or queries the current setting.
 Syntax :IMAGe:COLor {OFF|COLor|REVerse|
       GRAY}
       :IMAGe:COLor?
 Example :IMAGE:COLOR OFF
       :IMAGE:COLOR? -> :IMAGE:COLOR OFF
 Description This command is valid when the format
       (:IMAGe:FORMat) is not PSCRipt.
 :IMAGe:COMMent
 Function Sets the comment displayed at the bottom of the
       screen or queries the current setting.
 Syntax :IMAGe:COMMent {<String>}
       :IMAGe:COMMent?
       <String > = 25 characters or less (However, only
       the first 20 characters are displayed.)
 Example :IMAGE:COMMENT “THIS IS TEST.”
       :IMAGE:COMMENT? -> :IMAGE:
       COMMENT “THIS IS TEST.”
 :IMAGe:COMPression
 Function Enables or disables the data compression of
       screen image data in BMP format or queries the
       current setting.
 Syntax :IMAGe:COMPression {<Boolean>}
       :IMAGe:COMPression?
 Example :IMAGE:COMPRESSION ON
       :IMAGE:COMPRESSION? ->
       :IMAGE:COMPRESSION 1
 Description This command is valid when the format
       (:IMAGe:FORMat) is BMP and the color tone
       (:IMAGe:COLor) is {COLor|REVerse|GRAY}.
```
### Right column
```text
 :IMAGe:EXECute
 Function Saves the screen image data.
 Syntax :IMAGe:EXECute
 Example :IMAGE:EXECUTE

 :IMAGe:FORMat
 Function Sets the format of the screen image data to be
       saved or queries the current setting.
 Syntax :IMAGe:FORMat {TIFF|BMP|PSCRipt|
       PNG|JPEG}
       :IMAGe:FORMat?
 Example :IMAGE:FORMAT TIFF
       :IMAGE:FORMAT? ->
       :IMAGE:FORMAT TIFF
 :IMAGe:SAVE?
 Function Queries all settings related to the saving of
       screen image data.
 Syntax :IMAGe:SAVE?
 Example :IMAGE:SAVE? ->
       :IMAGE:SAVE:ANAMING 1;NAME “”

 :IMAGe:SAVE:ANAMing
 Function Sets whether to automatically name the screen
       image data files to be saved or queries the
       current setting.
 Syntax :IMAGe:SAVE:ANAMing {<Boolean>}
       :IMAGe:SAVE:ANAMing?
 Example :IMAGE:SAVE:ANAMING ON
       :IMAGE:SAVE:ANAMING? ->
       :IMAGE:SAVE:ANAMING 1
 :IMAGe:SAVE:CDIRectory
 Function Changes the save destination directory for the
       screen image data.
 Syntax :IMAGe:CDIRectory {<Filename>}
       <Filename> = Directory name
 Example :IMAGE:CDIRECTORY “IMAGE”
 Description Specify “..” to move up to the parent directory.
```

## Page 6-65

### Left column
```text
   :IMAGe:SAVE:DRIVe
   Function Sets the save destination drive of the screen
         image data.
   Syntax :IMAGe:SAVE:DRIVe {PCCard[,<NRf>]|
         NETWork|USB,<NRf>[,<NRf>][,<NRf>]}
         PCCard = PC card drive
         <NRf> = Partition (0 to 3)
         NETWork = Network drive
         USB = USB memory drive
         1st <NRf> = ID number (address)
         2nd <NRf> = Partition (0 to 3) or LUN (logical unit
         number: 0 to 3)
         3rd <NRf> = Partition (0 to 3) when LUN is
         specified
   Example :IMAGE:SAVE:DRIVE PCCARD
   Description • If the drive does not contain partitions, omit the
          <NRf> corresponding to partitions.
         • “NETWork” can be used when the Ethernet
          interface (/C7 option) is installed.
         • “USB” can be used when the USB port
          (peripheral device) (/C5 option) is installed.
         • The second or third <NRf> when USB is
          selected can be omitted if the drive is not
          partitioned or divided by LUN.
   :IMAGe:SAVE:NAME
   Function Sets the name of the file for saving the screen
         image data or queries the current setting.
   Syntax :IMAGe:SAVE:NAME {<Filename>}
         :IMAGe:SAVE:NAME?
   Example :IMAGE:SAVE:NAME “IMAGE1”
         :IMAGE:SAVE:NAME? ->
         :IMAGE:SAVE:NAME “IMAGE1”
   Description • Set the save destination drive with the
          “:IMAGe:SAVE:DRIVe” command and the
          directory with the
          “:IMAGe:SAVE:CDIRectory” command.
         • Specify the file name without the extension.
   :IMAGe:SEND?
   Function Queries the screen image data.
   Syntax :IMAGe:SEND?
   Example :IMAGE:SEND? -> #6(number of bytes,
         6 digits)(data byte sequence)
   Description • The number of bytes of <Block data> is {2 +
          6 + number of data points +1 (delimiter)}.
         • For details on <Block data>, see page 5-7.
```
### Right column
```text
                    6.13 IMAGe Group
```

## Page 6-66

### Section introduction
```text
   6.14   INPut  Group

 The commands in this group deal with the measurement condition of the input element.
 You can make the same settings and inquiries as when the keys in the measurement condition setup area (area
 enclosed in light blue), SCALING, LINE FILTER, FREQ FILTER (SHIFT+LINE FILTER), SYNC SOURCE, and
 NULL(SHIFT+SYNC SOURCE) on the front panel are used.

                                   [:INPut]:CFACtor
```
### Left column
```text
 :INPut?
 Function Queries all settings related to the input element.
 Syntax :INPut?
 Example :INPUT? -> :INPUT:CFACTOR 3;
       WIRING P1W2,P1W2,P1W2,P1W2;
       INDEPENDENT 0;VOLTAGE:RANGE:
       ELEMENT1 1.000E+03;
       ELEMENT2 1.000E+03;
       ELEMENT3 1.000E+03;
       ELEMENT4 1.000E+03;:INPUT:VOLTAGE:
       AUTO:ELEMENT1 0;ELEMENT2 0;
       ELEMENT3 0;ELEMENT4 0;:INPUT:
       VOLTAGE:MODE:ELEMENT1 RMS;
       ELEMENT2 RMS;ELEMENT3 RMS;
       ELEMENT4 RMS;:INPUT:CURRENT:RANGE:
       ELEMENT1 30.0E+00;
       ELEMENT2 30.0E+00;
       ELEMENT3 30.0E+00;
       ELEMENT4 30.0E+00;:INPUT:CURRENT:
       AUTO:ELEMENT1 0;ELEMENT2 0;
       ELEMENT3 0;ELEMENT4 0;:INPUT:
       CURRENT:MODE:ELEMENT1 RMS;
       ELEMENT2 RMS;ELEMENT3 RMS;
       ELEMENT4 RMS;:INPUT:CURRENT:SRATIO:
       ELEMENT1 10.0000;ELEMENT2 10.0000;
       ELEMENT3 10.0000;ELEMENT4 10.0000;:
       INPUT:FILTER:LINE:ELEMENT1 OFF;
       ELEMENT2 OFF;ELEMENT3 OFF;
       ELEMENT4 OFF;:INPUT:FILTER:
       FREQUENCY:ELEMENT1 0;ELEMENT2 0;
       ELEMENT3 0;ELEMENT4 0;:INPUT:
       SCALING:STATE:ELEMENT1 0;
       ELEMENT2 0;ELEMENT3 0;ELEMENT4 0;:
       INPUT:SCALING:VT:ELEMENT1 1.0000;
       ELEMENT2 1.0000;ELEMENT3 1.0000;
       ELEMENT4 1.0000;:INPUT:SCALING:CT:
       ELEMENT1 1.0000;ELEMENT2 1.0000;
       ELEMENT3 1.0000;ELEMENT4 1.0000;:
       INPUT:SCALING:SFACTOR:
       ELEMENT1 1.0000;ELEMENT2 1.0000;
       ELEMENT3 1.0000;ELEMENT4 1.0000;:
       INPUT:SYNCHRONIZE:ELEMENT1 I1;
       ELEMENT2 I2;ELEMENT3 I3;
       ELEMENT4 I4;:INPUT:NULL 0
```
### Right column
```text
 [:INPut]:CFACtor
 Function Sets the crest factor or queries the current
       setting.
 Syntax [:INPut]:CFACtor {<NRf>}
       [:INPut]:CFACtor?
       <NRf> = 3 or 6
 Example :INPUT:CFACTOR 3
       :INPUT:CFACTOR? -> :INPUT:CFACTOR 3
 [:INPut]:CURRent?
 Function Queries all settings related to the current
       measurement.
 Syntax [:INPut]:CURRent?
 Example :INPUT:CURRENT? -> :INPUT:CURRENT:
       RANGE:ELEMENT1 30.0E+00;
       ELEMENT2 30.0E+00;
       ELEMENT3 30.0E+00;
       ELEMENT4 30.0E+00;:INPUT:CURRENT:
       AUTO:ELEMENT1 0;ELEMENT2 0;
       ELEMENT3 0;ELEMENT4 0;:INPUT:
       CURRENT:MODE:ELEMENT1 RMS;
       ELEMENT2 RMS;ELEMENT3 RMS;
       ELEMENT4 RMS;:INPUT:CURRENT:SRATIO:
       ELEMENT1 10.0000;ELEMENT2 10.0000;
       ELEMENT3 10.0000;ELEMENT4 10.0000
 [:INPut]:CURRent:AUTO?
 Function Queries the current auto range setting (ON/OFF)
       of all elements.
 Syntax [:INPut]:CURRent:AUTO?
 Example :INPUT:CURRENT:AUTO? ->
       :INPUT:CURRENT:AUTO:ELEMENT1 0;
       ELEMENT2 0;ELEMENT3 0;ELEMENT4 0
 [:INPut]:CURRent:AUTO[:ALL]
 Function Collectively turns ON/OFF the current auto range
       of all elements.
 Syntax [:INPut]:CURRent:AUTO
       [:ALL] {<Boolean>}
 Example :INPUT:CURRENT:AUTO:ALL ON
```

## Page 6-67

### Left column
```text
   [:INPut]:CURRent:AUTO:ELEMent<x>
   Function Turns ON/OFF the current auto range of the
         element or queries the current setting.
   Syntax [:INPut]:CURRent:AUTO:
         ELEMent<x> {<Boolean>}
         [:INPut]:CURRent:AUTO:ELEMent<x>?
         <x> = 1 to 4 (element)
   Example :INPUT:CURRENT:AUTO:ELEMENT1 ON
         :INPUT:CURRENT:AUTO:ELEMENT1? ->
         :INPUT:CURRENT:AUTO:ELEMENT1 1
   [:INPut]:CURRent:AUTO:{SIGMA|SIGMB}
   Function Collectively turns ON/OFF the current auto range
         of all elements belonging to wiring unit {ΣA|ΣB}.
   Syntax [:INPut]:CURRent:AUTO:{SIGMA|
         SIGMB} {<Boolean>}
   Example :INPUT:CURRENT:AUTO:SIGMA ON
   Description • [:INPut]:CURRent:AUTO:SIGMA is valid
          only on models with 2 to 4 elements.
         • [:INPut]:CURRent:AUTO:SIGMB is valid
          only on models with 4 elements.
         • This command is invalid, if the wiring unit
          {SA|SB} does not exist as a result of the wiring
          system setting ([:INPut]:WIRing).
   [:INPut]:CURRent:MODE?
   Function Queries the current mode of all elements.
   Syntax [:INPut]:CURRent:MODE?
   Example :INPUT:CURRENT:MODE? ->
         :INPUT:CURRENT:MODE:ELEMENT1 RMS;
         ELEMENT2 RMS;ELEMENT3 RMS;
         ELEMENT4 RMS

   [:INPut]:CURRent:MODE[:ALL]
   Function Collectively sets the current mode of all elements.
   Syntax [:INPut]:CURRent:MODE[:ALL] {RMS|
         MEAN|DC|RMEAN}
   Example :INPUT:CURRENT:MODE:ALL RMS
   [:INPut]:CURRent:MODE:ELEMent<x>
   Function Sets the current mode of the element or queries
         the current setting.
   Syntax [:INPut]:CURRent:MODE:
         ELEMent<x> {RMS|MEAN|DC|RMEAN}
         [:INPut]:CURRent:MODE:ELEMent<x>?
         <x> = 1 to 4 (element)
   Example :INPUT:CURRENT:MODE:ELEMENT1 RMS
         :INPUT:CURRENT:MODE:ELEMENT1? ->
         :INPUT:CURRENT:MODE:ELEMENT1 RMS
```
### Right column
```text
                     6.14 INPut Group

 [:INPut]:CURRent:MODE:{SIGMA|SIGMB}
 Function Collectively sets the current mode of all elements
       belonging to wiring unit {ΣA|ΣB}.
 Syntax [:INPut]:CURRent:MODE:{SIGMA|
       SIGMB} {RMS|MEAN|DC|RMEAN}
 Example :INPUT:CURRENT:MODE:SIGMA RMS
 Description • [:INPut]:CURRent:MODE:SIGMA is valid
        only on models with 2 to 4 elements.
       • [:INPut]:CURRent:MODE:SIGMB is valid
        only on models with 4 elements.
       • This command is invalid, if the wiring unit
        {ΣA|ΣB} does not exist as a result of the wiring
        system setting ([:INPut]:WIRing).
 [:INPut]:CURRent:RANGe?
 Function Queries the current ranges of all elements.
 Syntax [:INPut]:CURRent:RANGe?
 Example :INPUT:CURRENT:RANGE? -> :INPUT:
       CURRENT:RANGE:ELEMENT1 30.0E+00;
       ELEMENT2 30.0E+00;
       ELEMENT3 30.0E+00;
       ELEMENT4 30.0E+00
 [:INPut]:CURRent:RANGe[:ALL]
 Function Collectively sets the current ranges of all
       elements.
 Syntax [:INPut]:CURRent:RANGe[:ALL]
       {<Current>|(EXTernal,<Voltage>)}
       When all the input elements of this instrument
       are 30 A input elements
       • When the crest factor is set to 3
        <Current> = 500 (mA), 1, 2, 5, 10, 20, 30 (A) (for
        direct current input)
        <Voltage> = 50, 100, 200, 500 (mV), 1, 2, 5, 10
        (V) (for external current sensor input)
       • When the crest factor is set to 6
        <Current> = 250, 500 (mA), 1, 2.5, 5, 10, 15 (A)
        (for direct current input)
        <Voltage> = 25, 50, 100, 250, 500 (mV), 1, 2.5,
        5 (V) (for external current sensor input)
       When all the input elements of this instrument
       are 2 A input elements
       • When crest factor is set to 3
        <Current> = 5, 10, 20, 50, 100, 200, 500 (mA),
        1, 2, (A) (with direct current input)
        <Voltage> = 50, 100, 200, 500 (mV), 1, 2, 5, 10
        (V) (with external current sensor input)
       • When crest factor is set to 6
        <Current> = 2.5, 5, 10, 25, 50, 100, 250, 500
        (mA), 1 (A) (with direct current input)
        <Voltage> = 25, 50, 100, 250, 500 (mV), 1, 2.5,
        5 (V) (with external current sensor input)
 Example :INPUT:CURRENT:RANGE:ALL 30A
       :INPUT:CURRENT:RANGE:
       ALL EXTERNAL,10V
 Description For models that have both 2 A input elements and
       30 A input elements installed, the direct current
       input range cannot be set collectively. Error 863
       will occur.
```

## Page 6-68

### Left column
```text
 6.14 INPut Group

 [:INPut]:CURRent:RANGe:ELEMent<x>
 Function Sets the current range of the element or queries
       the current setting.
 Syntax [:INPut]:CURRent:RANGe:ELEMent<x>
       {<Current>|(EXTernal,<Voltage>)}
       [:INPut]:CURRent:RANGe:ELEMent<x>?
       <x> = 1 to 4 (element)
       For the 30 A input element
       • When the crest factor is set to 3
        <Current> = 500 (mA), 1, 2, 5, 10, 20, 30 (A) (for
        direct current input)
        <Voltage> = 50, 100, 200, 500 (mV), 1, 2, 5, 10
        (V) (for external current sensor input)
       • When the crest factor is set to 6
        <Current> = 250, 500 (mA), 1, 2.5, 5, 10, 15 (A)
        (for direct current input)
        <Voltage> = 25, 50, 100, 250, 500 (mV), 1, 2.5,
        5 (V) (for external current sensor input)
       For the 2 A input element
       • When crest factor is set to 3
        <Current> = 5, 10, 20, 50, 100, 200, 500 (mA),
        1, 2, (A) (with direct current input)
        <Voltage> = 50, 100, 200, 500 (mV), 1, 2, 5, 10
        (V) (with external current sensor input)
       • When crest factor is set to 6
        <Current> = 2.5, 5, 10, 25, 50, 100, 250, 500
        (mA), 1 (A) (with direct current input)
        <Voltage> = 25, 50, 100, 250, 500 (mV), 1, 2.5,
        5 (V) (with external current sensor input)
 Example :INPUT:CURRENT:RANGE:ELEMENT1 30A
       :INPUT:CURRENT:RANGE:ELEMENT1? ->
       :INPUT:CURRENT:RANGE:
       ELEMENT1 30.0E+00
       :INPUT:CURRENT:RANGE:
       ELEMENT1 EXTERNAL,10V
       :INPUT:CURRENT:RANGE:ELEMENT1? ->
       :INPUT:CURRENT:RANGE:
       ELEMENT1 EXTERNAL,10.00E+00
```
### Right column
```text
 [:INPut]:CURRent:RANGe:{SIGMA|SIGMB}
 Function Collectively sets the current range of all elements
       belonging to wiring unit {ΣA|ΣB}.
 Syntax [:INPut]:CURRent:RANGe:{SIGMA|SIGMB}
       {<Current>|(EXTernal,<Voltage>)}
       For the 30 A input element
       • When the crest factor is set to 3
        <Current> = 500 (mA), 1, 2, 5, 10, 20, 30 (A) (for
        direct current input)
        <Voltage> = 50, 100, 200, 500 (mV), 1, 2, 5, 10
        (V) (for external current sensor input)
       • When the crest factor is set to 6
        <Current> = 250, 500 (mA), 1, 2.5, 5, 10, 15 (A)
        (for direct current input)
        <Voltage> = 25, 50, 100, 250, 500 (mV), 1, 2.5,
        5 (V) (for external current sensor input)
       For the 2 A input element
       • When crest factor is set to 3
        <Current> = 5, 10, 20, 50, 100, 200, 500 (mA),
        1, 2, (A) (with direct current input)
        <Voltage> = 50, 100, 200, 500 (mV), 1, 2, 5, 10
        (V) (with external current sensor input)
       • When crest factor is set to 6
        <Current> = 2.5, 5, 10, 25, 50, 100, 250, 500
        (mA), 1 (A) (with direct current input)
        <Voltage> = 25, 50, 100, 250, 500 (mV), 1, 2.5,
        5 (V) (with external current sensor input)
 Example :INPUT:CURRENT:RANGE:SIGMA 30A
 Description • [:INPut]:CURRent:RANGe:SIGMA is valid
        only on models with 2 to 4 elements.
       • [:INPut]:CURRent:RANGe:SIGMB is valid
        only on models with 4 elements.
       • This command is invalid, if the wiring unit
        {ΣA|ΣB} does not exist as a result of the wiring
        system setting ([:INPut]:WIRing).
```

## Page 6-69

### Left column
```text
   [:INPut]:CURRent:SRATio?
   Function Queries the current sensor scaling constants of
         all elements.
   Syntax [:INPut]:CURRent:SRATio?
   Example :INPUT:CURRENT:SRATIO? -> :INPUT:
         CURRENT:SRATIO:ELEMENT1 10.0000;
         ELEMENT2 10.0000;ELEMENT3 10.0000;
         ELEMENT4 10.0000
   [:INPut]:CURRent:SRATio[:ALL]
   Function Collectively sets the current sensor scaling
         constants of all elements.
   Syntax [:INPut]:CURRent:SRATio
         [:ALL] {<NRf>}
         <NRf> = 0.0001 to 99999.9999
   Example :INPUT:CURRENT:SRATIO:ALL 10

   [:INPut]:CURRent:SRATio:ELEMent<x>
   Function Sets the current sensor scaling constant of the
         element or queries the current setting.
   Syntax [:INPut]:CURRent:SRATio:
         ELEMent<x> {<NRf>}
         [:INPut]:CURRent:SRATio:ELEMent<x>?
         <x> = 1 to 4 (element)
         <NRf> = 0.0001 to 99999.9999
   Example :INPUT:CURRENT:SRATIO:ELEMENT1 10
         :INPUT:CURRENT:SRATIO:ELEMENT1? ->
         :INPUT:CURRENT:SRATIO:
         ELEMENT1 10.0000
   [:INPut]:FILTer?
   Function Queries all settings related to the filter.
   Syntax [:INPut]:FILTer?
   Example :INPUT:FILTER? -> :INPUT:FILTER:
         LINE:ELEMENT1 OFF;ELEMENT2 OFF;
         ELEMENT3 OFF;ELEMENT4 OFF;:INPUT:
         FILTER:FREQUENCY:ELEMENT1 0;
         ELEMENT2 0;ELEMENT3 0;ELEMENT4 0
   [:INPut]:FILTer:FREQuency?
   Function Queries the frequency filter settings of all
         elements.
   Syntax [:INPut]:FILTer:FREQuency?
   Example :INPUT:FILTER:FREQUENCY? ->
         :INPUT:FILTER:FREQUENCY:ELEMENT1 0;
         ELEMENT2 0;ELEMENT3 0;ELEMENT4 0
   [:INPut]:FILTer:FREQuency[:ALL]
   Function Collectively sets the frequency filter of all
         elements.
   Syntax [:INPut]:FILTer:FREQuency
         [:ALL] {<Boolean>}
   Example :INPUT:FILTER:FREQUENCY:ALL OFF
```
### Right column
```text
                     6.14 INPut Group

 [:INPut]:FILTer:FREQuency:ELEMent<x>
 Function Sets the frequency filter of the element or queries
       the current setting.
 Syntax [:INPut]:FILTer:FREQuency:
       ELEMent<x> {<Boolean>}
       [:INPut]:FILTer:FREQuency:
       ELEMent<x>?
       <x> = 1 to 4 (element)
 Example :INPUT:FILTER:FREQUENCY:ELEMENT1 ON
       :INPUT:FILTER:FREQUENCY:ELEMENT1?
       -> :INPUT:FILTER:FREQUENCY:
       ELEMENT1 1
 [:INPut]:FILTer:LINE?
 Function Queries the line filter settings of all elements.
 Syntax [:INPut]:FILTer:LINE?
 Example :INPUT:FILTER:LINE? ->
       :INPUT:FILTER:LINE:ELEMENT1 OFF;
       ELEMENT2 OFF;ELEMENT3 OFF;
       ELEMENT4 OFF
 [:INPut]:FILTer[:LINE][:ALL]
 Function Collectively sets the line filters of all elements.
 Syntax [:INPut]:FILTer[:LINE][:ALL]
       {OFF|<Frequency>}
       OFF = Line filter OFF
       <Frequency> = 500 Hz, 5.5 kHz, or 50 kHz (line
       filter ON, cutoff frequency)
 Example :INPUT:FILTER:LINE:ALL OFF

 [:INPut]:FILTer[:LINE]:ELEMent<x>
 Function Sets the line filter of the element or queries the
       current setting.
 Syntax [:INPut]:FILTer[:LINE]:
       ELEMent<x> {OFF|<Frequency>}
       [:INPut]:FILTer[:LINE]:ELEMent<x>?
       <x> = 1 to 4 (element)
       OFF = Line filter OFF
       <Frequency> = 500 Hz, 5.5 kHz, 50 kHz (line
       filter ON, cutoff frequency)
 Example :INPUT:FILTER:LINE:ELEMENT1 OFF
       :INPUT:FILTER:LINE:ELEMENT1? ->
       :INPUT:FILTER:LINE:ELEMENT1 OFF
 [:INPut]:INDependent
 Function Turns ON/OFF the independent setting of input
       elements or queries the current setting.
 Syntax [:INPut]:INDependent {<Boolean>}
       [:INPut]:INDependent?
 Example :INPUT:INDEPENDENT OFF
       :INPUT:INDEPENDENT? ->
       :INPUT:INDEPENDENT 0
 Description This command is valid only on models with 2 to 4
       elements.
```

## Page 6-70

### Left column
```text
 6.14 INPut Group

 [:INPut]:MODUle?
 Function Queries the input element type.
 Syntax [:INPut]:MODUle? {<NRf>}
       [:INPut]:MODUle?
       <NRf> = 1 to 4 (element)
 Example :INPUT:MODULE? 1 -> 30
       :INPUT:MODULE? -> 30,30,30,30
 Description • The response information is as follows:
           30 = (standard) power element (max.
       current range = 30 A)
           2 = low current range power element
       (max. current range = 2 A)
           0 = No input element
       • If the parameter is omitted, the input element
        types of all elements are output in order
        starting with element 1.
 [:INPut]:NULL
 Function Turns ON/OFF the NULL function or queries the
       current setting.
 Syntax [:INPut]:NULL {<Boolean>}
       [:INPut]:NULL?
 Example :INPUT:NULL ON
       :INPUT:NULL? -> :INPUT:NULL 1
 [:INPut]:POVer?
 Function Queries the peak over information.
 Syntax [:INPut]:POVer?
 Example :INPUT:POVER? -> 0
 Description • The peak over information of each element is
        mapped as shown below. A sum of decimal
        values of each bit is returned for the response.
       • For example, if the response is “16,” for
        example, peak over is occurring at U3.
         15 14 13 12 11 10 9 8 7 6 5 4 3 2 1 0
         0 0 Tq Sp 0 0 0 0 I4 U4 I3 U3 I2 U2 I1 U1
         Sp: Rotating speed
         Tq: Torque
 [:INPut]:SCALing?
 Function Queries all settings related to scaling.
 Syntax [:INPut]:SCALing?
 Example :INPUT:SCALING? -> :INPUT:SCALING:
       STATE:ELEMENT1 0;ELEMENT2 0;
       ELEMENT3 0;ELEMENT4 0;:INPUT:
       SCALING:VT:ELEMENT1 1.0000;
       ELEMENT2 1.0000;ELEMENT3 1.0000;
       ELEMENT4 1.0000;:INPUT:SCALING:CT:
       ELEMENT1 1.0000;ELEMENT2 1.0000;
       ELEMENT3 1.0000;ELEMENT4 1.0000;:
       INPUT:SCALING:SFACTOR:
       ELEMENT1 1.0000;ELEMENT2 1.0000;
       ELEMENT3 1.0000;ELEMENT4 1.0000
```
### Right column
```text
 [:INPut]:SCALing:{VT|CT|SFACtor}?
 Function Queries the {VT ratio|CT ratio|power factor} of all
       elements.
 Syntax [:INPut]:SCALing:{VT|CT|SFACtor}?
 Example :INPUT:SCALING:VT? ->
       :INPUT:SCALING:VT:ELEMENT1 1.0000;
       ELEMENT2 1.0000;ELEMENT3 1.0000;
       ELEMENT4 1.0000
 [:INPut]:SCALing:{VT|CT|SFACtor}
 [:ALL]
 Function Collectively sets the {VT ratio|CT ratio|power
       factor} of all elements.
 Syntax [:INPut]:SCALing:{VT|CT|SFACtor}
       [:ALL] {<NRf>}
       <NRf> = 0.0001 to 99999.9999
 Example :INPUT:SCALING:VT:ALL 1

 [:INPut]:SCALing:{VT|CT|SFACtor}:ELE
 Ment<x>
 Function Sets the {VT ratio|CT ratio|power factor} of the
       element or queries the current setting.
 Syntax [:INPut]:SCALing:{VT|CT|SFACtor}:
       ELEMent<x> {<NRf>}
       [:INPut]:SCALing:{VT|CT|SFACtor}:
       ELEMent<x>?
       <x> = 1 to 4 (element)
       <NRf> = 0.0001 to 99999.9999
 Example :INPUT:SCALING:VT:ELEMENT1 1
       :INPUT:SCALING:VT:ELEMENT1? ->
       :INPUT:SCALING:VT:ELEMENT1 1.0000
 [:INPut]:SCALing:STATe?
 Function Queries the scaling ON/OFF states of all
       elements.
 Syntax [:INPut]:SCALing:STATe?
 Example :INPUT:SCALING:STATE? ->
       :INPUT:SCALING:STATE:ELEMENT1 0;
       ELEMENT2 0;ELEMENT3 0;ELEMENT4 0
 [:INPut]:SCALing[:STATe][:ALL]
 Function Collectively turns ON/OFF the scaling of all
       elements.
 Syntax [:INPut]:SCALing[:STATe]
       [:ALL] {<Boolean>}
 Example :INPUT:SCALING:STATE:ALL OFF
```

## Page 6-71

### Left column
```text
   [:INPut]:SCALing[:STATe]:ELEMent<x>
   Function Turns ON/OFF the scaling of the element or
         queries the current setting.
   Syntax [:INPut]:SCALing[:STATe]:
         ELEMent<x> {<Boolean>}
         [:INPut]:SCALing[:STATe]:
         ELEMent<x>?
         <x> = 1 to 4 (element)
   Example :INPUT:SCALING:STATE:ELEMENT1 OFF
         :INPUT:SCALING:STATE:ELEMENT1? ->
         :INPUT:SCALING:STATE:ELEMENT1 0
   [:INPut]:SYNChronize?
   Function Queries the synchronization source of all
         elements.
   Syntax [:INPut]:SYNChronize?
   Example INPUT:SYNCHRONIZE? ->
         :INPUT:SYNCHRONIZE:ELEMENT1 I1;
         ELEMENT2 I2;ELEMENT3 I3;ELEMENT4 I4

   [:INPut]:SYNChronize[:ALL]
   Function Collectively sets the synchronization source of all
         elements.
   Syntax [:INPut]:SYNChronize[:ALL] {U<x>|
         I<x>|EXTernal|NONE}
         <x> = 1 to 4 (element)
         EXTernal = External clock input (Ext Clk)
         NONE = No synchronization source
   Example :INPUT:SYNCHRONIZE:ALL I1
   [:INPut]:SYNChronize:ELEMent<x>
   Function Sets the synchronization source of the element or
         queries the current setting.
   Syntax [:INPut]:SYNChronize:
         ELEMent<x> {U<x>|I<x>|EXTernal|
         NONE}
         [:INPut]:SYNChronize:ELEMent<x>?
         <x> = 1 to 4 (element)
         EXTernal = External clock input (Ext Clk)
         NONE = No synchronization source
   Example :INPUT:SYNCHRONIZE:ELEMENT1 I1
         :INPUT:SYNCHRONIZE:ELEMENT1? ->
         :INPUT:SYNCHRONIZE:ELEMENT1 I1
   [:INPut]:SYNChronize:{SIGMA|SIGMB}
   Function Collectively sets the synchronization source of all
         elements belonging to wiring unit {ΣA|ΣB}.
   Syntax [:INPut]:SYNChronize:{SIGMA|
         SIGMB} {U<x>|I<x>|EXTernal|NONE}
   Example :INPUT:SYNCHRONIZE:SIGMA I1
   Description • [:INPut]:SYNChronize:SIGMA is valid
          only on models with 2 to 4 elements.
         • [:INPut]:SYNChronize:SIGMB is valid
          only on models with 4 elements.
         • This command is invalid, if the wiring unit
          {ΣA|ΣB} does not exist as a result of the wiring
          system setting ([:INPut]:WIRing).
```
### Right column
```text
                     6.14 INPut Group

 [:INPut]:VOLTage?
 Function Queries all settings related to the voltage
       measurement.
 Syntax [:INPut]:VOLTage?
 Example :INPUT:VOLTAGE? -> :INPUT:VOLTAGE:
       RANGE:ELEMENT1 1.000E+03;
       ELEMENT2 1.000E+03;
       ELEMENT3 1.000E+03;
       ELEMENT4 1.000E+03;:INPUT:VOLTAGE:
       AUTO:ELEMENT1 0;ELEMENT2 0;
       ELEMENT3 0;ELEMENT4 0;:INPUT:
       VOLTAGE:MODE:ELEMENT1 RMS;
       ELEMENT2 RMS;ELEMENT3 RMS;
       ELEMENT4 RMS
 [:INPut]:VOLTage:AUTO?
 Function Queries the voltage auto range setting (ON/OFF)
       of all elements.
 Syntax [:INPut]:VOLTage:AUTO?
 Example :INPUT:VOLTAGE:AUTO? ->
       :INPUT:VOLTAGE:AUTO:ELEMENT1 0;
       ELEMENT2 0;ELEMENT3 0;ELEMENT4 0
 [:INPut]:VOLTage:AUTO[:ALL]
 Function Collectively turns ON/OFF the voltage auto range
       of all elements.
 Syntax [:INPut]:VOLTage:AUTO
       [:ALL] {<Boolean>}
 Example :INPUT:VOLTAGE:AUTO:ALL ON

 [:INPut]:VOLTage:AUTO:ELEMent<x>
 Function Turns ON/OFF the voltage auto range of the
       element or queries the current setting.
 Syntax [:INPut]:VOLTage:AUTO:
       ELEMent<x> {<Boolean>}
       [:INPut]:VOLTage:AUTO:ELEMent<x>?
       <x> = 1 to 4 (element)
 Example :INPUT:VOLTAGE:AUTO:ELEMENT1 ON
       :INPUT:VOLTAGE:AUTO:ELEMENT1? ->
       :INPUT:VOLTAGE:AUTO:ELEMENT1 1
 [:INPut]:VOLTage:AUTO:{SIGMA|SIGMB}
 Function Collectively turns ON/OFF the voltage auto range
       of all elements belonging to wiring unit {ΣA|ΣB}.
 Syntax [:INPut]:VOLTage:AUTO:{SIGMA|SIGMB}
       {<Boolean>}
 Example :INPUT:VOLTAGE:AUTO:SIGMA ON
 Description • [:INPut]:VOLTage:AUTO:SIGMA is valid
        only on models with 2 to 4 elements.
       • [:INPut]:VOLTage:AUTO:SIGMB is valid
        only on models with 4 elements.
       • This command is invalid, if the wiring unit
        {ΣA|ΣB} does not exist as a result of the wiring
        system setting ([:INPut]:WIRing).
```

## Page 6-72

### Left column
```text
 6.14 INPut Group

 [:INPut]:VOLTage:MODE?
 Function Queries the voltage mode of all elements.
 Syntax [:INPut]:VOLTage:MODE?
 Example :INPUT:VOLTAGE:MODE? ->
       :INPUT:VOLTAGE:MODE:ELEMENT1 RMS;
       ELEMENT2 RMS;ELEMENT3 RMS;
       ELEMENT4 RMS
 [:INPut]:VOLTage:MODE[:ALL]
 Function Collectively sets the voltage mode of all elements.
 Syntax [:INPut]:VOLTage:MODE[:ALL] {RMS|
       MEAN|DC|RMEAN}
 Example :INPUT:VOLTAGE:MODE:ALL RMS

 [:INPut]:VOLTage:MODE:ELEMent<x>
 Function Sets the voltage mode of the element or queries
       the current setting.
 Syntax [:INPut]:VOLTage:MODE:
       ELEMent<x> {RMS|MEAN|DC|RMEAN}
       [:INPut]:VOLTage:MODE:ELEMent<x>?
       <x> = 1 to 4 (element)
 Example :INPUT:VOLTAGE:MODE:ELEMENT1 RMS
       :INPUT:VOLTAGE:MODE:ELEMENT1? ->
       :INPUT:VOLTAGE:MODE:ELEMENT1 RMS
 [:INPut]:VOLTage:MODE:{SIGMA|SIGMB}
 Function Collectively sets the voltage mode of all elements
       belonging to wiring unit {ΣA|ΣB}.
 Syntax [:INPut]:VOLTage:MODE:{SIGMA|
       SIGMB} {RMS|MEAN|DC|RMEAN}
 Example :INPUT:VOLTAGE:MODE:SIGMA RMS
 Description • [:INPut]:VOLTage:MODE:SIGMA is valid
        only on models with 2 to 4 elements.
       • [:INPut]:VOLTage:MODE:SIGMB is valid
        only on models with 2 to 4 elements.
       • This command is invalid, if the wiring unit
        {ΣA|ΣB} does not exist as a result of the wiring
        system setting ([:INPut]:WIRing).
 [:INPut]:VOLTage:RANGe?
 Function Queries the voltage ranges of all elements.
 Syntax [:INPut]:VOLTage:RANGe?
 Example :INPUT:VOLTAGE:RANGE? ->
       :INPUT:VOLTAGE:RANGE:
       ELEMENT1 1.000E+03;
       ELEMENT2 1.000E+03;
       ELEMENT3 1.000E+03;
       ELEMENT4 1.000E+03
```
### Right column
```text
 [:INPut]:VOLTage:RANGe[:ALL]
 Function Collectively sets the voltage range of all elements.
 Syntax [:INPut]:VOLTage:RANGe[:ALL]
       {<Voltage>}
       • When the crest factor is set to 3
        <Voltage> = 15, 30, 60, 100, 150, 300, 600, or
        1000 (V)
       • When the crest factor is set to 6
        <Voltage> = 7.5, 15, 30, 50, 75, 150, 300, or
        500 (V)
 Example :INPUT:VOLTAGE:RANGE:ALL 1000V
 [:INPut]:VOLTage:RANGe:ELEMent<x>
 Function Sets the voltage range of the element or queries
       the current setting.
 Syntax [:INPut]:VOLTage:RANGe:
       ELEMent<x> {<Voltage>}
       [:INPut]:VOLTage:RANGe:ELEMent<x>?
       <x> = 1 to 4 (element)
       • When the crest factor is set to 3
        <Voltage> = 15, 30, 60, 100, 150, 300, 600, or
        1000 (V)
       • When the crest factor is set to 6
        <Voltage> = 7.5, 15, 30, 50, 75, 150, 300, or
        500 (V)
 Example :INPUT:VOLTAGE:RANGE:ELEMENT1 1000V
       :INPUT:VOLTAGE:RANGE:ELEMENT1?
       -> :INPUT:VOLTAGE:RANGE:ELEMENT1
       1.000E+03
 [:INPut]:VOLTage:RANGe:{SIGMA|SIGMB}
 Function Collectively sets the voltage range of all elements
       belonging to wiring unit {ΣA|ΣB}.
 Syntax [:INPut]:VOLTage:RANGe:{SIGMA|
       SIGMB} {<Voltage>}
       • When the crest factor is set to 3
        <Voltage> = 15, 30, 60, 100, 150, 300, 600, or
        1000 (V)
       • When the crest factor is set to 6
        <Voltage> = 7.5, 15, 30, 50, 75, 150, 300, or
        500 (V)
 Example :INPUT:VOLTAGE:RANGE:SIGMA 1000V
 Description • [:INPut]:VOLTage:RANGe:SIGMA is valid
        only on models with 2 to 4 elements.
       • [:INPut]:VOLTage:RANGe:SIGMB is valid
        only on models with 4 elements.
       • This command is invalid, if the wiring unit
        {ΣA|ΣB} does not exist as a result of the wiring
        system setting ([:INPut]:WIRing).
```

## Page 6-73

### Left column
```text
   [:INPut]:WIRing
   Function Sets the wiring system or queries the current
         setting.
   Syntax [:INPut]:WIRing {(P1W2|P1W3|P3W3|
         P3W4|V3A3)[,(P1W2|P1W3|P3W3|P3W4|
         V3A3|NONE)][,(P1W2|P1W3|P3W3|NONE)]
         [,(P1W2|NONE)]}
         [:INPut]:WIRing?
         P1W2 = Single-phase, two-wire system [1P2W]
         P1W3 = Single-phase, three-wire system [1P3W]
         P3W3 = Three-phase, three-wire system [3P3W]
         P3W4 = Three-phase, four-wire system [3P4W]
         V3A3 = Three-phase, three-wire (three-voltage,
         three-current) [3P3W(3V3A)]
         NONE = No wiring
   Example • Example for a 4-element model
          :INPUT:WIRING P1W2,P1W2,P1W2,P1W2
          :INPUT:WIRING? -> :INPUT:
          WIRING P1W2,P1W2,P1W2,P1W2
          :INPUT:WIRING P1W3,P3W3
          :INPUT:WIRING? ->
          :INPUT:WIRING P1W3,P3W3
         • Example for a 3-element model
          :INPUT:WIRING P3W3,P1W2
          :INPUT:WIRING? -> :INPUT:
          WIRING P3W3,P1W2
           :INPUT:WIRING P3W4
           :INPUT:WIRING? ->
           :INPUT:WIRING P3W4
   Description • Set the wiring system pattern in order starting
          from the element with the smallest number.
         • Some wiring system patterns may not be
          selectable depending on the model type. For
          details on the wiring system patterns, see the
          User’s Manual IM WT3001E-01EN.
         • The pattern is fixed to P1W2 on the 1-element
          model. All other settings are not allowed.
```
### Right column
```text
                     6.14 INPut Group
```

## Page 6-74

### Section introduction
```text
   6.15   INTEGrate    Group

 The commands in this group deal with integration.
 You can make the same settings and inquiries as when INTEG on the front panel is used.
```
### Left column
```text
 :INTEGrate?
 Function Queries all settings related to the integration.
 Syntax :INTEGrate?
 Example :INTEGRATE? -> :INTEGRATE:
       MODE NORMAL;ACAL 0;TIMER 1,0,0

 :INTEGrate:ACAL
 Function Turns ON/OFF the auto calibration or queries the
       current setting.
 Syntax :INTEGrate:ACAL {<Boolean>}
       :INTEGrate:ACAL?
 Example :INTEGRATE:ACAL OFF
       :INTEGRATE:ACAL? ->
       :INTEGRATE:ACAL 0
 :INTEGrate:MODE
 Function Sets the integration mode or queries the current
       setting.
 Syntax :INTEGrate:MODE {NORMal|CONTinuous|
       RNORmal|RCONtinuous}
       :INTEGrate:MODE?
       NORMal = Normal integration mode
       CONTinuous = Continuous integration mode
       RNORmal = Real-time normal integration mode
       RCONtinuous = Real-time continuous integration
       mode
 Example :INTEGRATE:MODE NORMAL
       :INTEGRATE:MODE? ->
       :INTEGRATE:MODE NORMAL
 :INTEGrate:RESet
 Function Resets the integrated value.
 Syntax :INTEGrate:RESet
 Example :INTEGRATE:RESET

 :INTEGrate:RTIMe?
 Function Queries the integration start and stop times for
       real-time integration mode.
 Syntax :INTEGrate:RTIMe<x>?
 Example :INTEGRATE:RTIME? ->
       :INTEGRATE:RTIME:
       START 2005,1,1,0,0,0;
       END 2005,1,1,1,0,0
```
### Right column
```text
 :INTEGrate:RTIMe:{STARt|END}
 Function Sets the integration {start|stop} time for real-time
       integration mode or queries the current setting.
 Syntax :INTEGrate:RTIMe:{STARt|
       END} {<NRf>,<NRf>,<NRf>,<NRf>,
       <NRf>,<NRf>}
       :INTEGrate:RTIMe:{STARt|END}?
       {<NRf>, <NRf>, <NRf>, <NRf>, <NRf>, <NRf>} =
       2001, 1, 1, 0, 0, 0 to 2099, 12, 31, 23, 59, 59
       1st <NRf> = 2001 to 2099 (year)
       2nd <NRf> = 1 to 12 (month)
       3rd <NRf> = 1 to 31 (day)
       4th <NRf> = 0 to 23 (hour)
       5th <NRf> = 0 to 59 (minute)
       6th <NRf> = 0 to 59 (second)
 Example :INTEGRATE:RTIME:
       START 2005,1,1,0,0,0
       :INTEGRATE:RTIME:START? ->
       :INTEGRATE:RTIME:
       START 2005,1,1,0,0,0
 :INTEGrate:STARt
 Function Starts integration.
 Syntax :INTEGrate:STARt
 Example :INTEGRATE:START
 :INTEGrate:STATe?
 Function Queries the integration condition.
 Syntax :INTEGrate:STATe?
 Example :INTEGRATE:STATE? -> RESET
 Description The response information is as follows:
       RESet = Integration reset
       READy = Waiting (real-time integration mode)
       STARt = Integration in progress
       STOP = Integration stop
       ERRor = Abnormal integration termination
       (integration overflow, power failure)
       TIMeup = Integration stop due to integration timer
       time
 :INTEGrate:STOP
 Function Stops integration.
 Syntax :INTEGrate:STOP
 Example :INTEGRATE:STOP
```

## Page 6-75

### Left column
```text
   :INTEGrate:TIMer<x>
   Function Sets the integration timer time or queries the
         current setting.
   Syntax :INTEGrate:TIMer {<NRf>,<NRf>,
         <NRf>}
         :INTEGrate:TIMer?
         {<NRf>, <NRf>, <NRf>} = 0, 0, 0 to 10000, 0, 0
         1st <NRf> = 0 to 10000 (hour)
         2nd <NRf> = 0 to 59 (minute)
         3rd <NRf> = 0 to 59 (second)
   Example :INTEGRATE:TIMER 1,0,0
         :INTEGRATE:TIMER? ->
         :INTEGRATE:TIMER 1,0,0
```
### Right column
```text
                  6.15 INTEGrate Group
```

## Page 6-76

### Section introduction
```text
   6.16   MEASure     Group

 The commands in this group deal with computation.
 You can make the same settings and inquiries as when MEASURE, AVG, “Frequency Meas. Item” menu of ITEM, and “η
 Formula,” “Compensation,” and “∆ Measure” menus of WIRING on the front panel are used.
```
### Left column
```text
 :MEASure?
 Function Queries all settings related to the computation.
 Syntax :MEASure?
 Example :MEASURE? -> :MEASURE:AVERAGING:
       STATE 0;TYPE EXPONENT;COUNT 2;:
       MEASURE:FREQUENCY:ITEM1 U1;
       ITEM2 I1;:MEASURE:SAMPLING AUTO;
       SQFORMULA TYPE1;PC:IEC 1976;
       P1 0.5000;P2 0.5000;:MEASURE:
       EFFICIENCY:ETA1 PB,PA;ETA2 PA,PB;
       ETA3 OFF;ETA4 OFF;UDEF1 P1;
       UDEF2 P1;:MEASURE:FUNCTION1:
       STATE 0;EXPRESSION “UMN(E1)”;
       UNIT “V”;:MEASURE:FUNCTION2:
       STATE 0;EXPRESSION “UMN(E2)”;
       UNIT “V”;:MEASURE:FUNCTION3:
       STATE 0;EXPRESSION “UMN(E3)”;
       UNIT “V”;:MEASURE:FUNCTION4:
       STATE 0;EXPRESSION “UMN(E4)”;
       UNIT “V”;:MEASURE:FUNCTION5:
       STATE 0;EXPRESSION “U(E1,ORT)”;
       UNIT “V”;:MEASURE:FUNCTION6:
       STATE 0;EXPRESSION “I(E1,ORT)”;
       UNIT “A”;:MEASURE:FUNCTION7:
       STATE 0;EXPRESSION “U(E1,ORT)”;
       UNIT “V”;:MEASURE:FUNCTION8:
       STATE 0;EXPRESSION “I(E1,ORT)”;
       UNIT “A”;:MEASURE:FUNCTION9:
       STATE 0;EXPRESSION “U(E1,ORT)”;
       UNIT “V”;:MEASURE:FUNCTION10:
       STATE 0;EXPRESSION “I(E1,ORT)”;
       UNIT “A”;:MEASURE:FUNCTION11:
       STATE 0;EXPRESSION “U(E1,ORT)”;
       UNIT “V”;:MEASURE:FUNCTION12:
       STATE 0;EXPRESSION “I(E1,ORT)”;
       UNIT “A”;:MEASURE:FUNCTION13:
       STATE 0;EXPRESSION “U(E1,ORT)”;
       UNIT “V”;:MEASURE:FUNCTION14:
       STATE 0;EXPRESSION “I(E1,ORT)”;
       UNIT “A”;:MEASURE:FUNCTION15:
       STATE 0;EXPRESSION “U(E1,ORT)”;
       UNIT “V”;:MEASURE:FUNCTION16:
       STATE 0;EXPRESSION “I(E1,ORT)”;
       UNIT “A”;:MEASURE:FUNCTION17:
       STATE 0;EXPRESSION “U(E1,ORT)”;
       UNIT “V”;:MEASURE:FUNCTION18:
       STATE 0;EXPRESSION “I(E1,ORT)”;
       UNIT “A”;:MEASURE:FUNCTION19:
       STATE 0;EXPRESSION “U(E1,ORT)”;
```
### Right column
```text
       UNIT “V”;:MEASURE:FUNCTION20:
       STATE 0;EXPRESSION “I(E1,ORT)”;
       UNIT “A”;:MEASURE:PHASE 180;
       SYNCHRONIZE MASTER;MHOLD 0;
       COMPENSATION:WIRING:ELEMENT1 OFF;
       ELEMENT2 OFF;ELEMENT3 OFF;
       ELEMENT4 OFF;:MEASURE:COMPENSATION:
       EFFICIENCY 0

 :MEASure:AVERaging?
 Function Queries all settings related to averaging.
 Syntax :MEASure:AVERaging?
 Example :MEASURE:AVERAGING? ->
       :MEASURE:AVERAGING:STATE 0;
       TYPE EXPONENT;COUNT 2
 :MEASure:AVERaging:COUNt
 Function Sets the averaging coefficient or queries the
       current setting.
 Syntax :MEASure:AVERaging:COUNt {<NRf>}
       :MEASure:AVERaging:COUNt?
       <NRf> = 2, 4, 8, 16, 32, 64 (attenuation constant
       when TYPE = EXPonent)
       <NRf> = 8, 16, 32, 64, 128, or 256 (moving
       average count when TYPE = LINear)
 Example :MEASURE:AVERAGING:COUNT 2
       :MEASURE:AVERAGING:COUNT? ->
       :MEASURE:AVERAGING:COUNT 2
 Description The averaging of measurement functions of
       harmonic measurement (option) is valid only
       when TYPE = EXPonent (attenuation constant).
       For details, see the User’s Manual IM WT3001E-
       01EN.
 :MEASure:AVERaging[:STATe]
 Function Turns ON/OFF averaging or queries the current
       setting.
 Syntax :MEASure:AVERaging
       [:STATe] {<Boolean>}
       :MEASure:AVERaging:STATe?
 Example :MEASURE:AVERAGING:STATE ON
       :MEASURE:AVERAGING:STATE? ->
       :MEASURE:AVERAGING:STATE 1
```

## Page 6-77

### Left column
```text
   :MEASure:AVERaging:TYPE
   Function Sets the averaging type or queries the current
         setting.
   Syntax :MEASure:AVERaging:TYPE {EXPonent|
         LINear}
         :MEASure:AVERaging:TYPE?
   Example :MEASURE:AVERAGING:TYPE EXPONENT
         :MEASURE:AVERAGING:TYPE? ->
         :MEASURE:AVERAGING:TYPE EXPONENT
   Description The averaging of measurement functions of
         harmonic measurement (option) is valid only for
         “EXPonent.” For details, see the User’s Manual
         IM WT3001E-01EN.
   :MEASure:COMPensation?
   Function Queries all settings related to the compensation
         computation.
   Syntax :MEASure:COMPensation?
   Example :MEASURE:COMPENSATION? ->
         :MEASURE:COMPENSATION:WIRING:
         ELEMENT1 OFF;ELEMENT2 OFF;
         ELEMENT3 OFF;ELEMENT4 OFF;:MEASURE:
         COMPENSATION:EFFICIENCY 0
   :MEASure:COMPensation:EFFiciency
   Function Turns ON/OFF the efficiency compensation or
         queries the current setting.
   Syntax :MEASure:COMPensation:
         EFFiciency {<Boolean>}
   Example :MEASURE:COMPENSATION:EFFICIENCY ON
         :MEASURE:COMPENSATION:EFFICIENCY? ->
         :MEASURE:COMPENSATION:
         EFFICIENCY 1
   :MEASure:COMPensation:V3A3
   Function Turns ON/OFF the compensation for the two-
         wattmeter method or queries the current setting.
   Syntax :MEASure:COMPensation:
         V3A3 {<Boolean>}
   Example :MEASURE:COMPENSATION:V3A3 ON
         :MEASURE:COMPENSATION:V3A3? ->
         :MEASURE:COMPENSATION:V3A3 1
   Description • This command is valid only on models with 3 to
          4 elements.
         • This command is valid when the wiring system
          ([:INPut]:WIRing) is set to V3A3.
```
### Right column
```text
                   6.16 MEASure Group

 :MEASure:COMPensation:WIRing?
 Function Queries all settings related to the wiring
       compensation.
 Syntax :MEASure:COMPensation:WIRing?
 Example :MEASURE:COMPENSATION:WIRING? ->
       :MEASURE:COMPENSATION:WIRING:
       ELEMENT1 OFF;ELEMENT2 OFF;
       ELEMENT3 OFF;ELEMENT4 OFF
 :MEASure:COMPensation:WIRing:ELEMent
 <x>
 Function Sets the wiring compensation of the element or
       queries the current setting.
 Syntax :MEASure:COMPensation:WIRing:
       ELEMent<x> {OFF|U_I|I_U}
       :MEASure:COMPensation:WIRing:
       ELEMent<x>?
       <x> = 1 to 4 (element)
 Example :MEASURE:COMPENSATION:WIRING:
       ELEMENT1 OFF
       :MEASURE:COMPENSATION:WIRING:
       ELEMENT1? -> :MEASURE:COMPENSATION:
       WIRING:ELEMENT1 OFF
 :MEASure:DMeasure?
 Function Queries all settings related to the delta
       computation.
 Syntax :MEASure:DMeasure?
 Example :MEASURE:DMEASURE? ->
       :MEASURE:DMEASURE:SIGMA OFF;
       SIGMB OFF
```

## Page 6-78

### Left column
```text
 6.16 MEASure Group

 :MEASure:DMeasure[:SIGMA]
 Function Sets the delta computation mode for wiring unit
       ΣA or queries the current setting.
 Syntax :MEASure:DMeasure[:SIGMA] {OFF|
       DIFFerence|P3W3_V3A3|ST_DT|DT_ST}
       :MEASure:DMeasure:SIGMA?
 Example :MEASURE:DMEASURE:SIGMA OFF
       :MEASURE:DMEASURE:SIGMA? ->
       :MEASURE:DMEASURE:SIGMA OFF
 Description The selections are as shown below: The
       wiring system of wiring unit ΣA determines the
       selectable modes.
       OFF = No delta computation (single-phase, two-
       wire system (1P2W) only)
       DIFFerence = Differential voltage, differential
       current (single-phase, three-wire system (1P3W),
       three-phase, three-wire system (3P3W) only)
       P3W3_V3A3 = 3P3W-to-3V3A conversion
       (single-phase, three-wire system (1P3W), three-
       phase, three-wire system (3P3W) only)
       ST_DT = Star-to-Delta conversion (three-phase,
       four-wire system (3P4W) only)
       DT_ST = Delta->Star conversion (three-phase,
       three-wire (three-voltage, three current) system
       [3P3W (3V3A)] only)
 :MEASure:DMeasure:SIGMB
 Function Sets the delta computation mode for wiring unit
       ΣB or queries the current setting.
 Syntax :MEASure:DMeasure:SIGMB {OFF|
       DIFFerence|P3W3_V3A3|ST_DT|DT_ST}
       :MEASure:DMeasure:SIGMB?
 Example :MEASURE:DMEASURE:SIGMB OFF
       :MEASURE:DMEASURE:SIGMB? ->
       :MEASURE:DMEASURE:SIGMB OFF
 Description The selections are the same as the
       “:MEASure:DMeasure[:SIGMA]” command.
       The wiring system of wiring unit ΣB determines
       the selectable modes.
 :MEASure:EFFiciency?
 Function Queries all settings related to the efficiency
       computation.
 Syntax :MEASure:EFFiciency?
 Example :MEASURE:EFFICIENCY? ->
       :MEASURE:EFFICIENCY:ETA1 PB,PA;
       ETA2 PA,PB;ETA3 OFF;ETA4 OFF;
       UDEF1 P1;UDEF2 P1
```
### Right column
```text
 :MEASure:EFFiciency:ETA<x>
 Function Sets the efficiency equation or queries the current
       setting.
 Syntax :MEASure:EFFiciency:ETA<x> {(OFF|
       P<x>|PA|PB|PM|UDEF<x>)[,(P<x>|PA|
       PB|PM|UDEF<x>)]}
       :MEASure:EFFiciency:ETA<x>?
       <x> of ETA<x> = 1 to 4 (η1 to η4)
       OFF = No computation (the denominator is
       ignored)
       <x> of P<x> = 1 to 4 (element)
       PA = PΣA (only on models with 2 to 4 elements)
       PB = PΣB (only on models with 4 elements)
       PM = Pm (motor output, only on models with the
       motor evaluation function (/MTR option))
       <x> of UDEF<x> = 1 to 2 (Udef1 to Udef2)
 Example :MEASURE:EFFICIENCY:ETA1 PB,PA
       :MEASURE:EFFICIENCY:ETA1? ->
       :MEASURE:EFFICIENCY:ETA1 PB,PA
 Description • Set the numerator and then the denominator.
       • The numerator can be omitted. The numerator
        is set to 1 when omitted.
       • The numerator is omitted when the numerator
        is 1 in the response to a query.
 :MEASure:EFFiciency:UDEF<x>
 Function Sets the user-defined parameter used in the
       efficiency equation or queries the current setting.
 Syntax :MEASure:EFFiciency:UDEF<x> {(NONE|
       P<x>|PA|PB|PM)[,(NONE|P<x>|PA|PB|
       PM)][,(NONE|P<x>|PA|PB|PM)][,(NONE|
       P<x>|PA|PB|PM)]}
       :MEASure:EFFiciency:UDEF<x>?
       <x> of UDEF<x> = 1 to 2 (Udef1 to Udef2)
       NONE = No parameters
       <x> of P<x> = 1 to 4 (element)
       PA = PΣA (only on models with 2 to 4 elements)
       PB = PΣB (only on models with 4 elements)
       PM = Pm (motor output, only on models with the
       motor evaluation function (/MTR option))
 Example :MEASURE:EFFICIENCY:UDEF1 P1,P2,P3
       :MEASURE:EFFICIENCY:UDEF1? ->
       :MEASURE:EFFICIENCY:UDEF1 P1,P2,P3
 Description • Set the parameters in the order parameter 1,
        parameter 2, parameter 3, and parameter 4.
       • Parameters 2 to 4 can be omitted. Omitted
        parameters are set to NONE.
       • Parameters are omitted when all of the
        subsequent parameters are NONE for
        parameters 2 to 4 in the response to a query.
```

## Page 6-79

### Left column
```text
   :MEASure:FREQuency?
   Function Queries all settings related to frequency
         measurement.
   Syntax :MEASure:FREQuency?
   Example :MEASURE:FREQUENCY? ->
         :MEASURE:FREQUENCY:ITEM1 U1;
         ITEM2 I1
   Description This command is invalid on models with the
         frequency measurement add-on (/FQ) option,
         because the frequency can be measured
         simultaneously on all input elements.
   :MEASure:FREQuency:ITEM<x>
   Function Sets the frequency measurement item or queries
         the current setting.
   Syntax :MEASure:FREQuency:ITEM<x> {U<x>|
         I<x>}
         :MEASure:FREQuency:ITEM<x>?
         <x> of ITEM<x> = 1 or 2 (Freq. 1 or Freq.2)
         <x> of U<x>, I<x> = 1 to 4 (element)
   Example :MEASURE:FREQUENCY:ITEM1 U1
         :MEASURE:FREQUENCY:ITEM1? ->
         :MEASURE:FREQUENCY:ITEM1 U1
   Description This command is invalid on models with the
         frequency measurement add-on (/FQ) option,
         because the frequency can be measured
         simultaneously on all input elements.
   :MEASure:FUNCtion<x>?
   Function Queries all settings related to user-defined
         functions.
   Syntax :MEASure:FUNCtion<x>?
         <x> = 1 to 20 (F1 to F20)
   Example :MEASURE:FUNCTION1? ->
         :MEASURE:FUNCTION1:STATE 1;
         EXPRESSION “UMN(E1)”;UNIT “V”
   :MEASure:FUNCtion<x>:EXPRession
   Function Sets the equation of the user-defined function or
         queries the current setting.
   Syntax :MEASure:FUNCtion<x>:EXPRession
         {<String>}
         :MEASure:FUNCtion<x>:EXPRession?
         <x> = 1 to 20 (F1 to F20)
         <String> = Up to 50 characters
   Example :MEASURE:FUNCTION1:
         EXPRESSION “UMN(E1)”
         :MEASURE:FUNCTION1:EXPRESSION? ->
         :MEASURE:FUNCTION1:
         EXPRESSION “UMN(E1)”
```
### Right column
```text
                   6.16 MEASure Group

 :MEASure:FUNCtion<x>[:STATe]
 Function Enables (ON) or Disables (OFF) the user-defined
       function or queries the current setting.
 Syntax :MEASure:FUNCtion<x>
       [:STATe] {<Boolean>}
       :MEASure:FUNCtion<x>:STATe?
       <x> = 1 to 20 (F1 to F20)
 Example :MEASURE:FUNCTION1:STATE ON
       :MEASURE:FUNCTION1:STATE? ->
       :MEASURE:FUNCTION1:STATE 1
 :MEASure:FUNCtion<x>:UNIT
 Function Sets the unit to be added to the computation
       result of the user-defined function or queries the
       current setting.
 Syntax :MEASure:FUNCtion<x>:UNIT {<String>}
       :MEASure:FUNCtion<x>:UNIT?
       <x> = 1 to 20 (F1 to F20)
       <String> = Up to 8 characters
 Example :MEASURE:FUNCTION1:UNIT “V”
       :MEASURE:FUNCTION1:UNIT? ->
       :MEASURE:FUNCTION1:UNIT “V”
 Description This command does not affect the computation
       result.
 :MEASure:MHOLd
 Function Enables (ON) or Disables (OFF) MAX HOLD
       function used in the user-defined function or
       queries the current setting.
 Syntax :MEASure:MHOLd {<Boolean>}
       :MEASure:MHOLd?
 Example :MEASURE:MHOLD ON
       :MEASURE:MHOLD? -> :MEASURE:MHOLD 1
 Description • The MAX HOLD operation starts when the
        MAX HOLD function is specified by the user-
        defined function and :MEASure:MHOLd is set
        to ON.
       • When :MEASure:MHOLd is set to OFF, the
        MAX HOLD operation terminates, and the MAX
        HOLD value becomes “no data.”
       • If ON is specified while :MEASure:MHOLd is
        ON, the MAX HOLD value is reset once, and
        the MAX HOLD operation starts again.
       • For details on the designation of the MAX
        HOLD function, see the User’s Manual IM
        WT3001E-01EN.
 :MEASure:PC?
 Function Queries all settings related to the computation of
       Pc (Corrected Power).
 Syntax :MEASure:PC?
 Example :MEASURE:PC? -> :MEASURE:PC:
       IEC 1976;P1 0.5000;P2 0.5000
 Description If the equation (:MEASure:PC:IEC) is set to
       2011, “IEC 1993” is returned as a response.
```

## Page 6-80

### Left column
```text
 6.16 MEASure Group

 :MEASure:PC:IEC
 Function Sets the equation used to compute Pc (Corrected
       Power) or queries the current setting.
 Syntax :MEASure:PC:IEC {<NRf>}
       :MEASure:PC:IEC?
       <NRf> = 1976, 1993 or 2011
 Example :MEASURE:PC:IEC 1976
       :MEASURE:PC:IEC? ->
       :MEASURE:PC:IEC 1976
 Description • Specify the year when the equation used to
        calculate the Pc was issued by IEC76-1.
       • If 2011 is specified, “IEC 1993” is returned as a
        response to a setting query.
 :MEASure:PC:P<x>
 Function Sets the parameter used to compute Pc
       (Corrected Power) or queries the current setting.
 Syntax :MEASure:PC:P<x> {<NRf>}
       :MEASure:PC:P<x>?
       <x> = 1, 2 (P1, P2)
       <NRf> = 0.0001 to 9.9999
 Example :MEASURE:PC:P1 0.5
       :MEASURE:PC:P1? ->
       :MEASURE:PC:P1 0.5000
 Description This parameter is used when the
       “:MEASure:PC:IEC” setting is set to
       “1976(IEC76-1(1976)).”
 :MEASure:PHASe
 Function Sets the display format of the phase difference or
       queries the current setting.
 Syntax :MEASure:PHASe {<NRf>}
       :MEASure:PHASe?
       <NRf> = 180 or 360
 Example :MEASURE:PHASE 180
       :MEASURE:PHASE? ->
       :MEASURE:PHASE 180
 Description Displays the phase using ±0 to 180° (Lead/Lag)
       for “180” and 0 to 360° for “360.”
 :MEASure:SAMPling
 Function Sets the sampling frequency or queries the
       current setting.
 Syntax :MEASure:SAMPling {AUTO|CLKA|CLKB|
       CLKC}
       :MEASure:SAMPling?
 Example :MEASURE:SAMPLING AUTO
       :MEASURE:SAMPLING? ->
       :MEASURE:SAMPLING AUTO
 Description For details on the sampling frequency
       corresponding to {AUTO|CLKA|CLKB|CLKC},
       see the User’s Manual IM WT3001E-01EN.
```
### Right column
```text
 :MEASure:SQFormula
 Function Sets the equation used to compute S (apparent
       power) and Q (reactive power) or queries the
       current setting.
 Syntax :MEASure:SQFormula {TYPE1|TYPE2|
       TYPE3}
       :MEASure:SQFormula?
 Example :MEASURE:SQFORMULA TYPE1
       :MEASURE:SQFORMULA? ->
       :MEASURE:SQFORMULA TYPE1
 Description • For details on the equation corresponding
        to {TYPE1|TYPE2|TYPE3}, see the User’s
        Manual IM WT3001E-01EN.
       • “TYPE3” is selectable only on models with the
        advanced computation function (/G6 option).
 :MEASure:SYNChronize
 Function Sets the synchronized measurement mode or
       queries the current setting.
 Syntax :MEASure:SYNChronize {MASTer|SLAVe}
       :MEASure:SYNChronize?
 Example :MEASURE:SYNCHRONIZE MASTER
       :MEASURE:SYNCHRONIZE? ->
       :MEASURE:SYNCHRONIZE MASTER
```

## Page 6-81

### Section introduction
```text
     6.17   MOTor    Group

   The commands in this group deal with the motor evaluation function.
   You can make the same settings and inquiries as when MOTOR SET (SHIFT+SCALING) on the front panel is used.
   However, the commands in this group are valid only on models with the motor evaluation function (/MTR option).
```
### Left column
```text
   :MOTor?
   Function Queries all settings related to the motor
         evaluation function.
   Syntax :MOTor?
   Example :MOTOR? -> :MOTOR:SPEED:
         TYPE ANALOG;RANGE 20.0E+00;AUTO 0;
         SCALING 1.0000;UNIT “rpm”;:MOTOR:
         TORQUE:TYPE ANALOG;RANGE 20.0E+00;
         AUTO 0;SCALING 1.0000;UNIT “Nm”;:
         MOTOR:PM:SCALING 1.0000;UNIT “W”;:
         MOTOR:FILTER:LINE OFF;:MOTOR:
         SYNCHRONIZE NONE;POLE 2;SSPEED I1
   :MOTor:FILTer?
   Function Queries all settings related to the input filter.
   Syntax :MOTor:FILTer?
   Example :MOTOR:FILTER? -> :MOTOR:FILTER:LINE
         OFF

   :MOTor:FILTer[:LINE]
   Function Sets the line filter or queries the current setting.
   Syntax :MOTor:FILTer[:LINE]
         {OFF|<Frequency>}
         :MOTor:FILTer:LINE?
         OFF = Line filter OFF
         <Frequency> = 100 Hz, 50 kHz (line filter ON,
         cutoff frequency)
   Example :MOTOR:FILTER:LINE OFF
         :MOTOR:FILTER:LINE? ->
         :MOTOR:FILTER:LINE OFF
   :MOTor:PM?
   Function Queries all settings related to the motor output
         (Pm).
   Syntax :MOTor:PM?
   Example :MOTOR:PM? -> :MOTOR:PM:
         SCALING 1.0000;UNIT “W”
   :MOTor:PM:SCALing
   Function Sets the scaling factor used for motor output
         computation or queries the current setting.
   Syntax :MOTor:PM:SCALing {<NRf>}
         :MOTor:PM:SCALing?
         <NRf> = 0.0001 to 99999.9999
   Example :MOTOR:PM:SCALING 1
         :MOTOR:PM:SCALING? ->
         :MOTOR:PM:SCALING 1.0000
```
### Right column
```text
 :MOTor:PM:UNIT
 Function Sets the unit to add to the motor output
       computation result or queries the current setting.
 Syntax :MOTor:PM:UNIT {<String>}
       :MOTor:PM:UNIT?
       <String> = Up to 8 characters
 Example :MOTOR:PM:UNIT “W”
       :MOTOR:PM:UNIT? ->
       :MOTOR:PM:UNIT “W”
 Description This command does not affect the computation
       result.
 :MOTor:POLE
 Function Sets the motor’s number of poles or queries the
       current setting.
 Syntax :MOTor:POLE {<NRf>}
       :MOTor:POLE?
       <NRf> = 1 to 99
 Example :MOTOR:POLE 2
       :MOTOR:POLE? -> :MOTOR:POLE 2

 :MOTor:SPEed?
 Function Queries all settings related to the rotating speed.
 Syntax :MOTor:SPEed?
 Example :MOTOR:SPEED? -> :MOTOR:SPEED:
       TYPE ANALOG;RANGE 20.0E+00;AUTO 0;
       SCALING 1.0000;UNIT “rpm”
 :MOTor:SPEed:AUTO
 Function Turns ON/OFF the voltage auto range of the
       revolution signal input (analog input format) or
       queries the current setting.
 Syntax :MOTor:SPEed:AUTO {<Boolean>}
       :MOTor:SPEed:AUTO?
 Example :MOTOR:SPEED:AUTO ON
       :MOTOR:SPEED:AUTO? ->
       :MOTOR:SPEED:AUTO 1
 Description This command is valid when the revolution signal
       input type (:MOTor:SPEed:TYPE) is “ANALog
       (analog input).”
```

## Page 6-82

### Left column
```text
 6.17 MOTor Group

 :MOTor:SPEed:PRANge
 Function Sets the range of the rotating speed (pulse input
       format) or queries the current setting.
 Syntax :MOTor:SPEed:PRANge {<NRf>,<NRf>}
       :MOTor:SPEed:PRANge?
       <NRf> = 0.0000 to 99999.9999
 Example :MOTOR:SPEED:PRANGE 10000,0
       :MOTOR:SPEED:PRANGE? -> :MOTOR:SPEED:
       PRANGE 10000.0000,0.0000
 Description • Set the upper limit and then the lower limit.
       • This command is valid when the revolution
        signal input type (:MOTor:SPEed:TYPE) is
        “PULSe (pulse input).”
 :MOTor:SPEed:PULSe
 Function Sets the pulse count of the revolution signal input
       (pulse input) or queries the current setting.
 Syntax :MOTor:SPEed:PULSe {<NRf>}
       :MOTor:SPEed:PULSe?
       <NRf> = 1 to 9999
 Example :MOTOR:SPEED:PULSE 60
       :MOTOR:SPEED:PULSE? ->
       :MOTOR:SPEED:PULSE 60
 Description This command is valid when the revolution signal
       input type (:MOTor:SPEed:TYPE) is “PULSe
       (pulse input).”
 :MOTor:SPEed:RANGe
 Function Sets the voltage range of the revolution signal
       input (analog input format) or queries the current
       setting.
 Syntax :MOTor:SPEed:RANGe {<Voltage>}
       :MOTor:SPEed:RANGe?
       <voltage> = 1, 2, 5, 10, or 20 (V)
 Example :MOTOR:SPEED:RANGE 20V
       :MOTOR:SPEED:RANGE? ->
       :MOTOR:SPEED:RANGE 20.0E+00
 Description This command is valid when the revolution signal
       input type (:MOTor:SPEed:TYPE) is “ANALog
       (analog input).”
 :MOTor:SPEed:SCALing
 Function Sets the scaling factor for rotating speed
       computation or queries the current setting.
 Syntax :MOTor:SPEed:SCALing {<NRf>}
       :MOTor:SPEed:SCALing?
       <NRf> = 0.0001 to 99999.9999
 Example :MOTOR:SPEED:SCALING 1
       :MOTOR:SPEED:SCALING? ->
       :MOTOR:SPEED:SCALING 1.0000
```
### Right column
```text
 :MOTor:SPEed:TYPE
 Function Sets the input type of the revolution signal input
       or queries the current setting.
 Syntax :MOTor:SPEed:TYPE {ANALog|PULSe}
       :MOTor:SPEed:TYPE?
 Example :MOTOR:SPEED:TYPE ANALOG
       :MOTOR:SPEED:TYPE? ->
       :MOTOR:SPEED:TYPE ANALOG
 :MOTor:SPEed:UNIT
 Function Sets the unit to add to the rotating speed
       computation result or queries the current setting.
 Syntax :MOTor:SPEed:UNIT {<String>}
       :MOTor:SPEed:UNIT?
       <String> = Up to 8 characters
 Example :MOTOR:SPEED:UNIT “rpm”
       :MOTOR:SPEED:UNIT? ->
       :MOTOR:SPEED:UNIT “rpm”
 Description This command does not affect the computation
       result.
 :MOTor:SSPeed(Sync SPeed source)
 Function Sets the frequency measurement source used
       to compute the synchronous speed (SyncSp) or
       queries the current setting.
 Syntax :MOTor:SSPeed {U<x>|I<x>}
       :MOTor:SSPeed?
       <x> = 1 to 4 (element)
 Example :MOTOR:SSPEED I1
       :MOTOR:SSPEED? -> :MOTOR:SSPEED I1

 :MOTor:SYNChronize
 Function Sets the synchronization source used to compute
       the rotating speed and torque or queries the
       current setting.
 Syntax :MOTor:SYNChronize {U<x>|I<x>|
       EXTernal|NONE}
       :MOTor:SYNChronize?
       <x> = 1 to 4 (element)
       EXTernal = External clock input (Ext Clk)
       NONE = No synchronization source
 Example :MOTOR:SYNCHRONIZE NONE
       :MOTOR:SYNCHRONIZE? ->
       :MOTOR:SYNCHRONIZE NONE
 :MOTor:TORQue?
 Function Queries all settings related to the torque.
 Syntax :MOTor:TORQue?
 Example :MOTOR:TORQUE? -> :MOTOR:TORQUE:
       TYPE ANALOG;RANGE 20.0E+00;AUTO 0;
       SCALING 1.0000;UNIT “Nm”
```

## Page 6-83

### Left column
```text
   :MOTor:TORQue:AUTO
   Function Turns ON/OFF the voltage auto range of the
         torque signal input (analog input format) or
         queries the current setting.
   Syntax :MOTor:TORQue:AUTO {<Boolean>}
         :MOTor:TORQue:AUTO?
   Example :MOTOR:TORQUE:AUTO ON
         :MOTOR:TORQUE:AUTO? ->
         :MOTOR:TORQUE:AUTO 1
   Description This command is valid when the torque signal
         input type (:MOTor:TORQue:TYPE) is “ANALog
         (analog input).”
   :MOTor:TORQue:PRANge
   Function Sets the range of the torque (pulse input format)
         or queries the current setting.
   Syntax :MOTor:TORQue:PRANge {<NRf>,<NRf>}
         :MOTor:TORQue:PRANge?
         <NRf> = –10000.0000 to 10000.0000
   Example :MOTOR:TORQUE:PRANGE 50,-50
         :MOTOR:TORQUE:PRANGE? ->
         :MOTOR:TORQUE:
         PRANGE 50.0000,-50.0000
   Description • Set the upper limit and then the lower limit.
         • This command is valid when the torque signal
          input type (:MOTor:TORQue:TYPE) is “PULSe
          (pulse input).”
   :MOTor:TORQue:RANGe
   Function Sets the voltage range of the torque signal input
         (analog input format) or queries the current
         setting.
   Syntax :MOTor:TORQue:RANGe {<Voltage>}
         :MOTor:TORQue:RANGe?
         <voltage> = 1, 2, 5, 10, or 20 (V)
   Example :MOTOR:TORQUE:RANGE 20V
         :MOTOR:TORQUE:RANGE? ->
         :MOTOR:TORQUE:RANGE 20.0E+00
   Description This command is valid when the torque signal
         input type (:MOTor:TORQue:TYPE) is “ANALog
         (analog input).”
   :MOTor:TORQue:RATE?
   Function Queries all settings related to the rated value of
         the torque signal (pulse input format).
   Syntax :MOTor:TORQue:RATE?
   Example :MOTOR:TORQUE:RATE? ->
         :MOTOR:TORQUE:RATE:
         UPPER 50.0000,15.000E+03;
         LOWER -50.0000,5.000E+03
```
### Right column
```text
                    6.17 MOTor Group

 :MOTor:TORQue:RATE:{UPPer|LOWer}
 Function Sets the rated value {upper limit|lower limit} of the
       torque signal (pulse input format) or queries the
       current setting.
 Syntax :MOTor:TORQue:RATE:{UPPer|
       LOWer} {<NRf>,<Frequency>}
       <NRf> = –10000.0000 to 10000.0000
       <Frequency> = 1 Hz to 100 MHz
 Example :MOTOR:TORQUE:RATE:UPPER 50,15kHz
       :MOTOR:TORQUE:RATE:UPPER?
       -> :MOTOR:TORQUE:RATE:UPPER
       50.0000,15.000E+03
 Description This command is valid when the torque signal
       input type (:MOTor:TORQue:TYPE) is “PULSe
       (pulse input).”
 :MOTor:TORQue:SCALing
 Function Sets the scaling factor used for torque
       computation or queries the current setting.
 Syntax :MOTor:TORQue:SCALing {<NRf>}
       :MOTor:TORQue:SCALing?
       <NRf> = 0.0001 to 99999.9999
 Example :MOTOR:TORQUE:SCALING 1
       :MOTOR:TORQUE:SCALING? ->
       :MOTOR:TORQUE:SCALING 1.0000
 :MOTor:TORQue:TYPE
 Function Sets the input type of the torque signal input or
       queries the current setting.
 Syntax :MOTor:TORQue:TYPE {ANALog|PULSe}
       :MOTor:TORQue:TYPE?
 Example :MOTOR:TORQUE:TYPE ANALOG
       :MOTOR:TORQUE:TYPE? ->
       :MOTOR:TORQUE:TYPE ANALOG
 :MOTor:TORQue:UNIT
 Function Sets the unit to add to the torque computation
       result or queries the current setting.
 Syntax :MOTor:TORQue:UNIT {<String>}
       :MOTor:TORQue:UNIT?
       <String> = Up to 8 characters
 Example :MOTOR:TORQUE:UNIT “Nm”
       :MOTOR:TORQUE:UNIT? ->
       :MOTOR:TORQUE:UNIT “Nm”
 Description This command does not affect the computation
       result.
```

## Page 6-84

### Section introduction
```text
   6.18   NUMeric    Group

 The commands in this group deal with numeric data output.
 There are no front panel keys that correspond to the commands in this group. The NUMERIC key on the front panel
 can be used to specify the same settings. The DISPlay group commands can be used to query the settings.
```
### Left column
```text
 :NUMeric?
 Function Queries all settings related to the numeric data
       output.
 Syntax :NUMeric?
 Example :NUMERIC? -> :NUMERIC:FORMAT ASCII;
       NORMAL:NUMBER 15;ITEM1 U,1,TOTAL;
       ITEM2 I,1,TOTAL;ITEM3 P,1,TOTAL;
       ITEM4 S,1,TOTAL;ITEM5 Q,1,TOTAL;
       ITEM6 LAMBDA,1,TOTAL;
       ITEM7 PHI,1,TOTAL;ITEM8 FU,1;
       ITEM9 FI,1;ITEM10 UPPEAK,1;
       ITEM11 UMPEAK,1;ITEM12 IPPEAK,1;
       ITEM13 IMPEAK,1;ITEM14 CFU,1;
       ITEM15 CFI,1;:NUMERIC:HOLD 0
 :NUMeric:CBCycle?
 Function Queries all settings related to output of numeric
       list data of Cycle by Cycle measurement.
 Syntax :NUMeric:CBCycle?
 Example :NUMERIC:CBCYCLE? ->
       :NUMERIC:CBCYCLE:ITEM U,1;
       START 1;END 100
 :NUMeric:CBCycle:END
 Function Sets the output end cycle of the numeric list data
       output by :NUMeric:CBCycle:VALue? or queries
       the current setting.
 Syntax :NUMeric:CBCycle:END {<NRf>}
       :NUMeric:CBCycle:END?
       <NRf> = 1 to 3000 (cycle number)
 Example :NUMERIC:CBCYCLE:END 100
       :NUMERIC:CBCYCLE:END ->
       :NUMERIC:CBCYCLE:END 100
```
### Right column
```text
 :NUMeric:CBCycle:ITEM
 Function Sets the numeric list data output items (function
       and element) of Cycle by Cycle measurement or
       queries the current setting.
 Syntax :NUMeric:CBCycle:ITEM {<Function>,
       <Element>}
       :NUMeric:CBCycle:ITEM?
       <Function> = {FREQ|U|I|P|S|Q|LAMBda|
       SPEed|TORQue|PM|PKU|PKI|PKSPeed|
       PKTorque}
       <Element> = {<NRf>|SIGMa|SIGMB} (<NRf>
        = 1 to 4)
 Example :NUMERIC:CBCYCLE:ITEM U,1
       :NUMERIC:CBCYCLE:ITEM? ->
       :NUMERIC:CBCYCLE:ITEM U,1
 Description • When <Function> = {FREQ|SPEed|
        TORQue|PM|PKSPeed|PKTorque},
        <Element> need not be specified. <Element>
        is omitted from the response.
       • When <Element> is omitted, Element 1 is set.
       • {SPEed|TORQue|PM|PKSPeed|
        PKTorque} is only available on models with
        the motor evaluation function (/MTR option).
 :NUMeric:CBCycle:STARt
 Function Sets the output start cycle of the numeric list data
       output by :NUMeric:CBCycle:VALue? or queries
       the current setting.
 Syntax :NUMeric:CBCycle:STARt {<NRf>}
       :NUMeric:CBCycle:STARt?
       <NRf> = 1 to 3000 (cycle number)
 Example :NUMERIC:CBCYCLE:START 1
       :NUMERIC:CBCYCLE:START ->
       :NUMERIC:CBCYCLE:START 1
```

## Page 6-85

### Left column
```text
   :NUMeric:CBCycle:VALue?
   Function Queries the numeric list data from Cycle by Cycle
         measurement.
   Syntax :NUMeric:CBCycle:VALue?
         {<Function>,<Element>}
         :NUMeric:CBCycle:VALue?
         <Function> = {FREQ|U|I|P|S|Q|LAMBda|
         SPEed|TORQue|PM|PKU|PKI|PKSPeed|
         PKTorque}
         <Element> = {<NRf>|SIGMa|SIGMB} (<NRf>
          = 1 to 4)
   Example • Example when parameters specified
          (For :NUMeric:CBCycle:STARt 1;END
          100)
          :NUMERIC:CBCYCLE:VALUE? U,1 ->
          100.001E+00,100.002E+00,
          100.003E+00,100.004E+00,
          ..(ommitted)..,100.099E+00,
          100.100E+00
         • Example when parameters omitted
          (For :NUMeric:CBCycle:ITEM U,1)
          :NUMERIC:CBCYCLE:VALUE? ->
          100.001E+00,100.002E+00,
          100.003E+00,100.004E+00,
          ..(ommitted)..,100.099E+00,
          100.100E+00
         • Example in which “:NUMeric:FORMat” is set
          to FLOat.
          :NUMERIC:CBCYCLE:VALUE? -> #6
          (number of bytes, six digits) (data byte
          sequence)
   Description • Numeric list data consists of up to 3000 numeric
          data from “:NUMeric:CBCycle:STARt” to
          “:Numeric:CBCycle:END”.
         • If a parameters are specified, the numeric
          list data of that item is output. For a
          description of the contents of <Function>
          and <Element>, see the description for
          “:NUMeric:CBCycle:ITEM”.
         • If the parameter is omitted, the numeric
          list data for the items specified in
          “:NUMeric:CBCycle:ITEM” is output.
         • For the format of the individual numeric data
          that are output, see “Numeric Data Format” at
          the end of this group (page 6-97).
```
### Right column
```text
                   6.18 NUMeric Group

 :NUMeric:FLICker?
 Function Queries all settings related to output of numeric
       data from flicker measurement.
 Syntax :NUMeric:FLICker?
 Example :NUMERIC:FLICKER? -> :NUMERIC:
       FLICKER:FUNCTION:NUMBER 8;
       ITEM1 TIME;ITEM2 UN,1;ITEM3 FU,1;
       ITEM4 DC,1,CURRENT;ITEM5 DMAX,1,
       CURRENT;ITEM6 DT,1,CURRENT;
       ITEM7 PST,1,CURRENT;ITEM8 PLT,1;:
       NUMERIC:FLICKER:INFORMATION:
       NUMBER 7;ITEM1 JTOTAL,TOTAL;
       ITEM2 JDC,1,ALL;ITEM3 JDMAX,1,ALL;
       ITEM4 JDT,1,ALL;ITEM5 JPST,1,ALL;
       ITEM6 JPLT,1;ITEM7 JTOTAL,1
 Description Only available with the flicker measurement
       function (/FL option).
 :NUMeric:FLICker:COUNt?
 Function Queries the number of the measurement within
       the specified observation period at which flicker
       measurement stops.
 Syntax :NUMeric:FLICker:COUNt?
 Example :NUMERIC:FLICKER:COUNT? -> 0
 Description • Only available with the flicker measurement
         function (/FL option).
       • Returns the number displayed on the right of
         the Count bar graph in the flicker measurement
         display screen.
 :NUMeric:FLICker:FUNCtion?
 Function Queries all settings related to output of measured
       flicker data (variable format).
 Syntax :NUMeric:FLICker:FUNCtion?
 Example :NUMERIC:FLICKER:FUNCTION? ->
       :NUMERIC:FLICKER:FUNCTION:NUMBER 8;
       ITEM1 TIME;ITEM2 UN,1;ITEM3 FU,1;
       ITEM4 DC,1,CURRENT;ITEM5 DMAX,1,
       CURRENT;ITEM6 DT,1,CURRENT;
       ITEM7 PST,1,CURRENT;ITEM8 PLT,1
 Description • Only available with the flicker measurement
         function (/FL option).
       • For the values of
         “:NUMeric:FLICker:FUNCtion:ITEM<x>”,
         only the number of numeric data output items
         specified in
         “:NUMeric:FLICker:FUNCtion:NUMber”
         are output.
```

## Page 6-86

### Left column
```text
 6.18 NUMeric Group

 :NUMeric:FLICker:FUNCtion:CLEar
 Function Clears (sets to NONE) the output items of
       measured flicker data (variable format).
 Syntax :NUMeric:FLICker:FUNCtion:
       CLEar {ALL|<NRf>[,<NRf>]}
       ALL = Clears all items
       1st <NRf> = 1 to 32 (item number to start
       clearing)
       2nd <NRf> = 1 to 32 (item number to stop
       clearing)
 Example :NUMERIC:FLICKER:FUNCTION:CLEAR ALL
 Description • Only available with the flicker measurement
        function (/FL option).
       • If the 2nd <NRf> is omitted, the output items
        from the start clear number to the last item (32)
        are cleared.
 :NUMeric:FLICker:FUNCtion:DELete
 Function Deletes the output items of measured flicker data
       (variable format).
 Syntax :NUMeric:FLICker:FUNCtion:
       DELete {<NRf>[,<NRf>]}
       1st <NRf> = 1 to 32 (item number to start
       deleting)
       2nd <NRf> = 1 to 32 (item number to stop
       deleting)
 Example :NUMERIC:FLICKER:FUNCTION:DELETE 1
       (Deletes ITEM1 and shifts ITEM2 and subsequent
       items forward)
       :NUMERIC:FLICKER:FUNCTION:
       DELETE 1,3
       (Deletes ITEM1 to 3 and shifts ITEM4 and
       subsequent items forward)
 Description • Only available with the flicker measurement
        function (/FL option).
       • Output items subsequent to the deleted output
        items are shifted in order into the deleted items’
        position, and NONE is set in the open positions
        on the end.
       • If the 2nd <NRf> is omitted, only the output
        item of the start delete number is deleted.
 :NUMeric:FLICker:FUNCtion:ITEM<x>
 Function Sets output items (function, element, and
       observation period) of measured flicker data
       (variable format) or queries the current setting.
 Syntax :NUMeric:FLICker:FUNCtion:
       ITEM<x> {NONE|<Function>,
       <Element>[,<Period>]}
       :NUMeric:FLICker:FUNCtion:ITEM<x>?
       <x> = 1 to 32 (item number)
       NONE = No output items
       <Function> = {TIME|UN|FU|DC|DMAX|DT|
       TMAX|PST|PLT}
       <Element> = {<NRf>} (<NRf> = 1 to 4)
       <Period> = {CURRent|<NRf>|ALL}
       (<NRf> = 1 to 99)
```
### Right column
```text
 Example :NUMERIC:FLICKER:FUNCTION:
       ITEM1 DC,1,1
       :NUMERIC:FLICKER:FUNCTION:ITEM1? ->
       :NUMERIC:FLICKER:FUNCTION:
       ITEM1 DC,1,1
 Description • Only available with the flicker measurement
        function (/FL option).
       • The contents that are output for each of the
        selections for <Function> are as follows:
 <Function>       <Element> <Period>
 Output Contents  Designation Designation
 TIME
   Elapsed measurement time [sec] Not required Not required
   (the time displayed under Flicker: in the upper right part of
   the screen)
 UN
   RMS voltage (rated voltage) Un[V] Required Not required
 FU
   Voltage frequency Freq[Hz] Required Not required
 DC
   Relative steady-state voltage Required Required
   change dc[%]
 DMAX
   Maximum relative voltage Required Required
   change dmax[%]
 DT
   Relative voltage change time Required Required
   d(t)[ms]
 TMAX
   Tmax[ms]       Required Required
 PST
   Short-term flicker value Pst Required Required
 PLT
   Long-term flicker value Plt Required Not required
       • When <Element> is omitted, Element 1 is set.
       • The contents of the selections for <Period> are
        as follows. If <Period> is omitted, CURRent is
        set.
        CURRent The observation period
        currently being measured (rows of the numeric
        list marked with an asterisk (*) in the flicker
        measurement display screen).
        When in measurement complete status, same
        as ALL.
        ALL Overall observation period (Result row
        of the numeric list in the flicker measurement
        display screen).
        <NRf> = 1 to 99 Specified observation period.
       • <Element> or <Period> is omitted from the
        response to the output items in the table
        above for which specification of <Element> or
        <Period> is not required.
       • TMAX, a new function defined in IEC61000-
        3-3 Ed3.0, can be used. TMAX represents the
        same content as the conventional DT function,
        and the measured data that is output is also
        the same.
```

## Page 6-87

### Left column
```text
         • For IEC61000-3-3 Ed3.0, “TMAX” is returned
          as a response to a setting query.

   :NUMeric:FLICker:FUNCtion:NUMber
   Function Sets the number of measured flicker data output
         by “:NUMeric:FLICker:FUNCtion:VALue?” or
         queries the current setting.
   Syntax :NUMeric:FLICker:FUNCtion:
         NUMber {<NRf>|ALL}
         :NUMeric:FLICker:FUNCtion:NUMber?
         <NRf> = 1 to 32(ALL)
   Example :NUMERIC:FLICKER:FUNCTION:NUMBER 8
         :NUMERIC:FLICKER:FUNCTION:NUMBER ->
         :NUMERIC:FLICKER:FUNCTION:NUMBER 8
   Description • Only available with the flicker measurement
          function (/FL option).
         • If parameters are omitted from “:NUMeric:F
          LICker:FUNCtion:VALue?”, numeric data
          from 1 to (specified value) is output in order.
         • The initial setting for the number of numeric
          data is 8.
   :NUMeric:FLICker:FUNCtion:VALue?
   Function Queries the measured flicker data (variable
         format).
   Syntax :NUMeric:FLICker:FUNCtion:
         VALue? {<NRf>}
         :NUMeric:FLICker:FUNCtion:VALue?
         <NRf> = 1 to 32 (item number)
   Example • Example when <NRf> is specified
          :NUMERIC:FLICKER:FUNCTION:
          VALUE? 4 -> 1.52E+00
         • Example when <NRf> is omitted
          :NUMERIC:FLICKER:FUNCTION:
          VALUE? -> 600,229.75E+00,
          50.000E+00,1.52E+00,1.56E+00,
          3E+00,0.43E+00,0.17E+00
         • Example in which “:NUMeric:FORMat” is set to
          “FLOat”.
          :NUMERIC:FLICKER:FUNCTION:VALUE?
          -> #4 (number of bytes, four digits) (data
          byte sequence)
   Description • Only available with the flicker measurement
          function (/FL option).
         • When <NRf> is specified, only the numeric
          data for that item is output.
```
### Right column
```text
                   6.18 NUMeric Group

       • If <NRf> is omitted, numeric data from the item
        number in “:NUMeric:FLICker:FUNCtion:
        NUMber” is output in order.
       • The format of individual numeric data that is
        output is as follows:
        (1) Data when normal
       • Elapsed measurement time (TIME)
        ASCII: <NR1> format in units of seconds
        (Example :for 1 hour (1:00:00), 3600)
        FLOAT: IEEE single-precision floating
        point (4-byte) format in units of seconds
        (Example :for 1 hour (1:00:00), 0x45610000)
       • No items (NONE)
        ASCII: “NAN” (Not A Number)
        FLOAT: 0x7E951BEE (9.91E+37)
       • Other than above
        ASCII: <NR3> format (mantissa, 5 digits;
        exponent, 2 digits, Example :229.87E+00)
        FLOAT: IEEE single-precision floating
        point (4-byte) format
        (2) Error Data
       • Data does not exist (display: “-----”)
        ASCII: “NAN” (Not A Number)
        FLOAT: 0x7E951BEE (9.91E+37)
       • Overrange (display: “-O-L-”)
       • Overflow (display: “-O-F-”)
       • Data over (display: “Error”)
       • No steady-state condition (display: “Undef”)
        ASCII: “INF” (INFinity)
        FLOAT: 0x7E94F56A (9.9E+37)
 :NUMeric:FLICker:INFOrmation?
 Function Queries all settings related to output of flicker
       judgment results (variable format).
 Syntax :NUMeric:FLICker:INFOrmation?
 Example :NUMERIC:FLICKER:INFORMATION? ->
       :NUMERIC:FLICKER:INFORMATION:
       NUMBER 7;ITEM1 JTOTAL,TOTAL;
       ITEM2 JDC,1,ALL;ITEM3 JDMAX,1,ALL;
       ITEM4 JDT,1,ALL;ITEM5 JPST,1,ALL;
       ITEM6 JPLT,1;ITEM7 JTOTAL,1
 Description • Only available with the flicker measurement
        function (/FL option).
       • For the values of
        “:NUMeric:FLICker:INFOrmation:
        ITEM<x>”, only the number of
        numeric data output items specified in
        “:NUMeric:FLICker:FUNCtion:
        INFOrmation:NUMber” are output.
```

## Page 6-88

### Left column
```text
 6.18 NUMeric Group

 :NUMeric:FLICker:INFOrmation:CLEar
 Function Clears (sets to NONE) the output items of flicker
       judgment results (variable format).
 Syntax :NUMeric:FLICker:INFOrmation:
       CLEar {ALL|<NRf>[,<NRf>]}
       ALL = Clears all items
       1st <NRf> = 1 to 32 (item number to start
       clearing)
       2nd <NRf> = 1 to 32 (item number to stop
       clearing)
 Example :NUMERIC:FLICKER:INFORMATION:
       CLEAR ALL
 Description • Only available with the flicker measurement
        function (/FL option).
       • If the 2nd <NRf> is omitted, the output items
        from the start clear number to the last item (32)
        are cleared.
 :NUMeric:FLICker:INFOrmation:DELete
 Function Deletes the output items of flicker judgment
       results (variable format).
 Syntax :NUMeric:FLICker:INFOrmation:
       DELete {<NRf>[,<NRf>]}
       1st <NRf> = 1 to 32 (item number to start
       deleting)
       2nd <NRf> = 1 to 32 (item number to stop
       deleting)
 Example :NUMERIC:FLICKER:INFORMATION:
       DELETE 1
       (Deletes ITEM1 and shifts ITEM2 and subsequent
       items forward)
       :NUMERIC:FLICKER:INFORMATION:
       DELETE 1,3
       (Deletes ITEM1Å|3 and shifts ITEM4 and
       subsequent items forward)
 Description • Only available with the flicker measurement
        function (/FL option).
       • Output items subsequent to the deleted output
        items are shifted in order into the deleted items’
        position, and NONE is set in the open positions
        on the end.
       • If the 2nd <NRf> is omitted, only the output
        item of the start delete number is deleted.
```
### Right column
```text
 :NUMeric:FLICker:INFOrmation:ITEM<x>
 Function Sets the output items (function, element, and
       observation period) of flicker judgment results
       (variable format) or queries the current setting.
 Syntax :NUMeric:FLICker:INFOrmation:
       ITEM<x> {NONE|<Function>,
       <Element>[,<Period>]}
       :NUMeric:FLICker:INFOrmation:
       ITEM<x>?
       <x> = 1 to 32 (item number)
       NONE = No output items
       <Function> = {JTOTal|JDC|JDMAX|JDT|
       JTMAX|JPST|JPLT}
       <Element> = {<NRf>|TOTal} (<NRf> = 1 to 4)
       <Period> = {<NRf>|ALL} (<NRf> = 1 to 99)
 Example :NUMERIC:FLICKER:INFORMATION:
       ITEM1 JDC,1,1
       :NUMERIC:FLICKER:INFORMATION:
       ITEM1? -> :NUMERIC:FLICKER:
       INFORMATION:ITEM1 JDC,1,1
 Description • Only available with the flicker measurement
        function (/FL option).
       • The contents that are output for each of the
        selections for <Function> are as follows:
 <Function>
   Output Contents <Element> <Period>
                  Designation Designation
 JTOTal
   Overall judgment results for dc, Required Not required
   dmax, d(t)*, pst, and plt
   (the judgment results displayed under [Element# Judgment:]
   in the upper right part of the screen)
 JDC
   Judgment results for relative Required Required
   steady-state voltage change dc
 JDMAX
   Judgment results for maximum Required Required
   relative voltage change dmax
 JDT
   Judgment results for relative Required Required
   voltage change time d(t)
 JTMAX
   Judgment results for Tmax Required Required
 JPST
   Judgment results for short-term Required Required
   flicker value Pst
 JPLT
   Judgment results for long-term Required Not required
   flicker value Plt
       * Tmax for IEC 61000-3-3 Edition 3.0, d(t) for
        IEC 61000-3-3 Edition 2.0.
```

## Page 6-89

### Left column
```text
         • The contents of the selections for <Element>
          are as follows. When <Element> is omitted,
          Element 1 is set.
          TOTal The overall judgment result for all
              measured elements is only available
              when <Function> = JTOTal (judgment
              result displayed under [Total Judgment:]
              in the upper right part of the screen)
          <NRf> = 1 to 4 specified elements
         • The contents of the selections for <Period> are
          as follows.
          If <Period> is omitted, ALL is set.
          ALL Overall observation period (Result row
          of the numeric list in the flicker measurement
          display screen)
          <NRf> = 1 to 99 specified observation periods
         • <Period> is omitted from the response to
          output items in the table above for which
          specification of <Period> is not required.
         • JTMAX, a new function defined in IEC61000-3-
          3 Ed3.0, can be used. JTMAX represents the
          same content as the conventional DT function,
          and the judgment results that is output is also
          the same.
         • For IEC61000-3-3 Ed3.0, “JTMAX” is returned
          as a response to a setting query.
   :NUMeric:FLICker:INFOrmation:NUMber
   Function Sets the number of flicker judgment results output
         by “:NUMeric:FLICker:INFOrmation:VALue?” or
         queries the current setting.
   Syntax :NUMeric:FLICker:INFOrmation:
         NUMber {<NRf>|ALL}
         :NUMeric:FLICker:INFOrmation:
         NUMber?
         <NRf> = 1 to 32(ALL)
   Example :NUMERIC:FLICKER:INFORMATION:
         NUMBER 7
         :NUMERIC:FLICKER:INFORMATION:
         NUMBER -> :NUMERIC:FLICKER:
         FUNCTION:NUMBER 7
   Description • Only available with the flicker measurement
          function (/FL option).
         • If parameters are omitted from “:NUMeric:
          FLICker:INFOrmation:VALue?”, judgment
          results from 1 to (specified value) are output in
          order.
         • The initial setting for the number of judgment
          results is 7.
```
### Right column
```text
                   6.18 NUMeric Group

 :NUMeric:FLICker:INFOrmation:VALue?
 Function Queries the judgment results (variable format).
 Syntax :NUMeric:FLICker:INFOrmation:
       VALue? {<NRf>}
       :NUMeric:FLICker:INFOrmation:VALue?
       <NRf> = 1 to 32 (item number)
 Example • Example when <NRf> is specified
        :NUMERIC:FLICKER:INFORMATION:
        VALUE? 1 -> 0
       • Example when <NRf> is omitted
        :NUMERIC:FLICKER:INFORMATION:
        VALUE? -> 0,0,0,0,0,0,0
       • Example in which “:NUMeric:FORMat” is set
        to “FLOat”.
        :NUMERIC:FLICKER:INFORMATION:
        VALUE? -> #4 (number of bytes, four digits)
        (data byte sequence)
 Description • Only available with the flicker measurement
        function (/FL option).
       • When <NRf> is specified, only the judgment
        results for that item is output.
       • If <NRf> is omitted, judgment results from the
        item number in
        “:NUMeric:FLICker:INFOrmation:
        NUMber” is output in order.
       • The format of individual judgment results that
        are output is as follows:
       • Judgment result (JTOTal, JDC, JDMAX,
        JDT, JPST, JPLT)
      ASCII    FLOAT
      (<NR1> format) (IEEE single-precision floating
               point (4-byte) format)
 Pass: “0”     0x00000000 (0)
 Fail: “-1”    0xBF800000 (-1)
 Error: “-2”   0xC0000000 (-2)
 -----: “1”    0x3F800000 (1)
 (space): “1”  0x3F800000 (1)
       • No items (NONE)
        ASCII: “NAN” (Not A Number)
        FLOAT: 0x7E951BEE (9.91E+37)
```

## Page 6-90

### Left column
```text
 6.18 NUMeric Group

 :NUMeric:FLICker:JUDGement?
 Function Queries the judgment results (fixed format).
 Syntax :NUMeric:FLICker:JUDGement? {<NRf>|
       ALL}
       :NUMeric:FLICker:JUDGement?
       <NRf> = 1 to9 (observation period number)
       ALL = Overall observation period (Result)
 Example • Example in which “:NUMeric:FORMat” is set
        to “ASCii”
        :NUMERIC:FLICKER:JUDGEMENT? 1 ->
        0,0,0,0,0,0,0,-1,-1,-1,-1,-1,-1,
        -1,-1,-1,-1,-1,-1
       • Example in which :NUMeric:FORMat is set to
        “FLOat”.
        :NUMERIC:FLICKER:JUDGEMENT? -> #4
        (number of bytes, four digits) (data byte
        sequence)
 Description • Only available with the flicker measurement
        function (/FL option).
       • The contents and order of the judgment results
        that are output are in the fixed format below.
        To modify the output contents and order, use
        the “:NUMeric:FLICker:INFOrmation”
        commands.
```
### Right column
```text
       Output contents and order of Judgment results
       For function names, see the description for “:NUM
       eric:FLICker:INFOrmation:ITEM<x>”.
       Numbers refer to elements. (ALL) is the overall
       judgment result for all measured elements.
         JTOTal(ALL)→
         JDC1→JDMAX1→JDT1*→JPST1→
         JPLT1→JTOTal1→
         JDC2→JDMAX2→JDT2*→JPST2→
         JPLT2→JTOTal12→(output only for 2 to
         4 element models)
         JDC3→JDMAX3→JDT3*→JPST3→
         JPLT3→JTOTal13→ (output only for 3 to 4
         element models)
         JDC4→JDMAX4→JDT4*→JPST4→
         JPLT4→JTOTal14→ (output only for 4
         element models)
       * JTMAX1, JTMAX2, JTMAX3, or JTMAX4 for
        IEC 61000-3-3 Edition 3.0, JDT1, JDT2, JDT3,
        or JDT4 for IEC 61000-3-3 Edition 2.0.
       • For 1 element models, 7 data from JTOTal(ALL)
        to JTOTal1 are output.
        For 2 element models, 13 data from
        JTOTal(ALL) to JTOTal2 are output.
        For 3 element models, 19 data from
        JTOTal(ALL) to JTOTal3 are output.
        For 4 element models, 25 data from
        JTOTal(ALL) to JTOTal4 are output.
       • If parameters are specified, the judgment
        results of the specified observation period are
        output.
       • If parameters are omitted, the judgment result
        of the overall observation period (Result) is
        output (the same output occurs as when the
        ALL parameters are specified).
       • For the format of individual numeric data, see
        the description for “:NUMeric:FLICker:INF
        Ormation:VALue?”.
 :NUMeric:FLICker:PERiod?
 Function Queries the observation period number currently
       being measured during flicker measurement.
 Syntax :NUMeric:FLICker:PERiod?
 Example :NUMERIC:FLICKER:PERIOD? -> 5
 Description • Only available with the flicker measurement
        function (/FL option).
       • Returns the observation period numbers
        marked with an asterisk (*) in the No. column
        of the numeric list in the flicker measurement
        screen. If no asterisks are displayed (such
        as after a reset or during initialization), 0 is
        returned.
```

## Page 6-91

### Left column
```text
   :NUMeric:FLICker:VALue?
   Function Queries the measured flicker data (fixed format).
   Syntax :NUMeric:FLICker:VALue? {<NRf>|ALL}
         :NUMeric:FLICker:VALue?
         <NRf> = 1 to 99 (observation period number)
         ALL = Overall observation period (Result)
   Example • Example in which “:NUMeric:FORMat” is set
          to “ASCii”.
          :NUMERIC:FLICKER:VALUE? 1 ->
          600,229.75E+00,50.000E+00,
          1.52E+00,1.56E+00,3E+00,...
         • Example in which “:NUMeric:FORMat” is set
          to “FLOat”.
          :NUMERIC:FLICKER:VALUE? -> #4
          (number of bytes, four digits) (data byte
          sequence)
   Description • Only available with the flicker measurement
          function (/FL option).
         • The contents and order of the numeric data
          that are output are in the following fixed format.
          To modify the output contents and order,
          use the “:NUMeric:FLICker:FUNCtion”
          commands.
         Output contents and order of numeric data
         For function names, see the description for “:NUM
         eric:FLICker:FUNCtion:ITEM<x>”.
         Numbers refer to elements.
            TIME→
            UN1→FU1→DC1→DMAX1→DT1*→
            PST1→PLT1→
            UN2→FU2→DC2→DMAX2→DT*2→
            PST2→PLT2→ (output only for 2 to 4
            element models)
            UN3→FU3→DC3→DMAX3→DT3*→
            PST3→PLT3→ (output only for 3 to 4
            element models)
            UN4→FU4→DC4→DMAX4→DT4*→
            PST4→PLT4→ (output only for 4
            element models)
         * TMAX1, TMAX2, TMAX3, or TMAX4 for IEC
          61000-3-3 Edition 3.0, DT1, DT2, DT3, or DT4
          for IEC 61000-3-3 Edition 2.0.
         • For 1 element models, 8 data from TIME to
          PLT1 are output.
          For 2 element models, 15 data from TIME to
          PLT2 are output.
          For 3 element models, 22 data from TIME to
          PLT3 are output.
          For 4 element models, 29 data from TIME to
          PLT4 are output.
         • If the parameters are specified, the numeric
          data of the specified observation period is
          output.
```
### Right column
```text
                   6.18 NUMeric Group

       • If the parameters are omitted, the measured
        data of the current observation period being
        measured is output. When in measurement
        complete status, the measured data of the
        overall observation period (Result) is output.
       • For the format of individual numeric data, see
        the description for “:NUMeric:FLICker:FUN
        Ction:VALue?”.
 :NUMeric:FORMat
 Function Sets the format of the numeric data that is
       transmitted by “:NUMeric[:NORMal]:VALue?” or
       “:NUMeric:LIST:VALue?” or queries the current
       setting.
 Syntax :NUMeric:FORMat {ASCii|FLOat}
       :NUMeric:FORMat?
 Example :NUMERIC:FORMAT ASCII
       :NUMERIC:FORMAT? ->
       :NUMERIC:FORMAT ASCII
 Description • The format of the numeric data that is output
        varies depending on the “:NUMeric:FORMat”
        setting as follows:
        (1) When “ASCii” is specified
           Outputs the physical value in <NR3>
           format (<NR1> format only for the elapsed
           time of integration (TIME)).
           The data of each item is delimited by a
           comma.
        (2) When “FLOat” is specified
           A 6-byte or 8-byte header (example
           “#40060” or “#6000408”) is added in front
           of the numeric data block. The physical
           value in IEEE single-precision floating
           point (4-byte) format follows the header.
           The byte order of the data of each item is
           MSB First.
       • For the format of the individual numeric data,
        see “Numeric Data Format” at the end of this
        group of commands (see page 6-97).
```

## Page 6-92

### Left column
```text
 6.18 NUMeric Group

 :NUMeric:HOLD
 Function Sets whether to hold (ON) or release (OFF) all
       the numeric data or queries the current setting.
 Syntax :NUMeric:HOLD {<Boolean>}
       :NUMeric:HOLD?
 Example :NUMERIC:HOLD ON
       :NUMERIC:HOLD? -> :NUMERIC:HOLD 1
 Description • If :NUMeric:HOLD is turned ON before
        executing “:NUMeric[:NORMal]:VALue?” or
        “:NUMeric:LIST:VALue?,” all the numeric
        data at that point can be held internally.
       • As long as :NUMeric:HOLD is ON, the
        numeric data is held even when the numeric
        data on the screen is updated.
       • For example, if you wish to retrieve various
        types of numeric data of each element at the
        same point, do the following:
        :NUMeric:HOLD ON
        :NUMeric[:NORMal]:ITEM1 U,1,TOTAL;
        ITEM2 I,1,TOTAL;... (set the numeric
        data items of element 1)
        :NUMeric[:NORMal]:VALue?
        (Receive the numeric data of element 1)
        :NUMeric[:NORMal]:ITEM1 U,2,TOTAL;
        ITEM2 I,2,TOTAL;... (set the numeric
        data items of element 2)
        :NUMeric[:NORMal]:VALue?
        (Receive the numeric data of element 2)
        ...(omitted)...
        :NUMeric[:NORMal]:ITEM1 U,4,TOTAL;
        ITEM2 I,4,TOTAL;... (set the numeric
        data items of element 4)
        :NUMeric[:NORMal]:VALue?
        (Receive the numeric data of element 4)
        :NUMeric:HOLD OFF
       • If ON is specified when :NUMeric:HOLD is
        ON, the numeric data is cleared once, and the
        most recent numeric data is held internally.
        This method can be used when retrieving
        numeric data continuously (no need to set
        :NUMeric:HOLD to OFF each time).
```
### Right column
```text
 :NUMeric:LIST?
 Function Queries all settings related to the numeric list
       data output of harmonic measurement.
 Syntax :NUMeric:LIST?
 Example :NUMERIC:LIST? ->
       :NUMERIC:LIST:NUMBER 1;
       ORDER 100;SELECT ALL;ITEM1 U,1
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • For the values of
        “:NUMeric:LIST:ITEM<x>,” the numeric list
        data output items for the amount specified by
        “:NUMeric:LIST:NUMber” are output.
 :NUMeric:LIST:CLEar
 Function Clears the output items of the numeric list data of
       harmonic measurement (set to “NONE”).
 Syntax :NUMeric:LIST:CLEar {ALL|
       <NRf>[,<NRf>]}
       ALL = Clear all items
       1st <NRf> = 1 to 64 (Item number to start
       clearing)
       2nd <NRf> = 1 to 64 (Item number to end
       clearing)
 Example :NUMERIC:LIST:CLEAR ALL
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • If the 2nd <NRf> is omitted, the output items
        from the start clear number to the last item (64)
        are cleared.
```

## Page 6-93

### Left column
```text
   :NUMeric:LIST:DELete
   Function Deletes the output items of the numeric list data
         of harmonic measurement.
   Syntax :NUMeric:LIST:DELete {<NRf>
         [,<NRf>]}
         1st <NRf> = 1 to 64 (Item number to start
         deleting)
         2nd <NRf> = 1 to 64 (Item number to end
         deleting)
   Example :NUMERIC:LIST:CLEAR 1 (Deletes ITEM1
         and shift ITEM2 and subsequent items
         forward)
         :NUMERIC:LIST:CLEAR 1,3 (Deletes ITEM1
         to ITEM3 and shift ITEM4 and subsequent items
         forward)
   Description • This command is valid only on models with the
          advanced computation function (/G6 option).
         • The subsequent output items fill the positions
          of deleted output items, and empty sections at
          the end are set to “NONE.”
         • If the 2nd <NRf> is omitted, only the output
          item of the delete start number is deleted.
   :NUMeric:LIST:ITEM<x>
   Function Sets the output items (function elements) of the
         numeric list data of harmonic measurement or
         queries the current setting.
   Syntax :NUMeric:LIST:ITEM<x> {NONE|
         <Function>,<Element>}
         :NUMeric:LIST:ITEM<x>?
         <x> = 1 to 64 (item number)
         NONE = No output item
         <Function> = {U|I|P|S|Q|LAMBda|PHI|
         PHIU|PHII|Z|RS|XS|RP|XP|UHDF|IHDF|
         PHDF}
         <Element> = {<NRf>|SIGMa|SIGMB} (<NRf>
         = 1 to 4)
   Example :NUMERIC:LIST:ITEM1 U,1
         :NUMERIC:LIST:ITEM1? ->
         :NUMERIC:LIST:ITEM1 U,1
   Description This command is valid only on models with the
         advanced computation function (/G6 option).
```
### Right column
```text
                   6.18 NUMeric Group

 :NUMeric:LIST:NUMber
 Function Sets the number of the numeric list data that
       is transmitted by “:NUMeric:LIST:VALue?” or
       queries the current setting.
 Syntax :NUMeric:LIST:NUMber {<NRf>|ALL}
       :NUMeric:LIST:NUMber?
       <NRf> = 1 to 64 (ALL)
 Example :NUMERIC:LIST:NUMBER 5
       :NUMERIC:LIST:NUMBER ->
       :NUMERIC:LIST:NUMBER 5
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • If the parameter is omitted for the
        “:NUMeric:LIST:VALue?” command, the
        numeric list data from 1 to (the specified value)
        is output in order.
       • By default, the number of numeric data is set to
        “1.”
 :NUMeric:LIST:ORDer
 Function Sets the maximum output order of the numeric
       list data of harmonic measurement or queries the
       current setting.
 Syntax :NUMeric:LIST:ORDer {<NRf>|ALL}
       :NUMeric:LIST:ORDer?
       <NRf> = 1 to 100(ALL)
 Example :NUMERIC:LIST:ORDER 100
       :NUMERIC:LIST:ORDER? ->
       :NUMERIC:LIST:ORDER 100
 Description This command is valid only on models with the
       advanced computation function (/G6 option).
 :NUMeric:LIST:PRESet
 Function Sets the output items of harmonic measurement
       numeric list data to a preset pattern.
 Syntax :NUMeric:LIST:PRESet {<NRf>}
       <NRf> = 1 to 4
 Example :NUMERIC:LIST:PRESET 1
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • For details on the output items that are preset,
        see “(2) Preset Pattern of the Numeric List
        Data Output Items of Harmonic Measurement ”
        (see page 6-100).
       • By default, output items of “Pattern 2” is
        selected.
```

## Page 6-94

### Left column
```text
 6.18 NUMeric Group

 :NUMeric:LIST:SELect
 Function Sets the output component of the numeric list
       data of harmonic measurement or queries the
       current setting.
 Syntax :NUMeric:LIST:SELect {EVEN|ODD|ALL}
       :NUMeric:LIST:SELect?
 Example :NUMERIC:LIST:SELECT ALL
       :NUMERIC:LIST:SELECT? ->
       :NUMERIC:LIST:SELECT ALL
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • The selections are as shown below:
        EVEN = Outputs the components of TOTal,
        DC, and even order harmonic
        ODD = Outputs the components of TOTal, DC,
        and odd order harmonic
        ALL = Outputs all components
```
### Right column
```text
 :NUMeric:LIST:VALue?
 Function Queries the numeric list data of harmonic
       measurement.
 Syntax :NUMeric:LIST:VALue? {<NRf>}
       <NRf> = 1 to 64 (item number)
 Example • Example when <NRf> is specified
        :NUMERIC:LIST:VALUE? 1 ->
        103.58E+00,0.00E+00,103.53E+00,
        0.09E+00,2.07E+00,0.04E+00,
        ..(omitted)..,0.01E+00,0.01E+00 (up to
        102 items of data)
       • Example when <NRf> is omitted (when
        “:NUMeric:LIST:NUMber” is 5)
        :NUMERIC:LIST:VALUE? ->
        103.58E+00,0.00E+00,103.53E+00,
        0.09E+00,2.07E+00,0.04E+00,
        ..(omitted)..,0.00E+00,0.00E+00 (up to
        102*5 = 510 items of data)
       • Example in which “:NUMeric:FORMat” is set
        to “FLOat”
        :NUMERIC:LIST:VALUE? -> #6(number of
        bytes, 6 digits)(data byte sequence)
 Description • This command is valid only on models with the
        advanced computation function (/G6 option).
       • A single numeric list data consists of
        up to 102 items of numeric data in the
        following order: TOTal, DC, 1st order, ...
        “:NUMeric:LIST:ORDer.”
       • If <NRf> is specified, only the numeric list data
        of the item number is output (up to 102 items of
        data).
       • If <NRf> is omitted, the numeric
        list data of item numbers from 1 to
        “:NUMeric:LIST:NUMber” is output in order
        (up to 102*”:NUMeric:LIST:NUMber” items
        of data).
       • For the format of the individual numeric data
        that is output, see “Numeric Data Format” at
        the end of this group of commands (see page
        6-97).
```

## Page 6-95

### Left column
```text
   :NUMeric:NORMal?
   Function Queries all settings related to the numeric data
         output.
   Syntax :NUMeric:NORMal?
   Example :NUMERIC:NORMAL? -> :NUMERIC:
         NORMAL:NUMBER 15;ITEM1 U,1,TOTAL;
         ITEM2 I,1,TOTAL;ITEM3 P,1,TOTAL;
         ITEM4 S,1,TOTAL;ITEM5 Q,1,TOTAL;
         ITEM6 LAMBDA,1,TOTAL;
         ITEM7 PHI,1,TOTAL;ITEM8 FU,1;
         ITEM9 FI,1;ITEM10 UPPEAK,1;
         ITEM11 UMPEAK,1;ITEM12 IPPEAK,1;
         ITEM13 IMPEAK,1;ITEM14 CFU,1;
         ITEM15 CFI,1
   Description For the values of
         “:NUMeric[:NORMal]:ITEM<x>,” the numeric
         data output items for the amount specified by
         “:NUMeric[:NORMal]:NUMber” are output.
   :NUMeric[:NORMal]:CLEar
   Function Clears the numeric data output item (sets
         “NONE”).
   Syntax :NUMeric[:NORMal]:CLEar {ALL|
         <NRf>[,<NRf>]}
         ALL = Clear all items
         1st <NRf> = 1 to 255 (Item number to start
         clearing)
         2nd <NRf> = 1 to 255 (Item number to end
         clearing)
   Example :NUMERIC:NORMAL:CLEAR ALL
   Description If the 2nd <NRf> is omitted, the output items from
         the start clear number to the last item (255) are
         cleared.
   :NUMeric[:NORMal]:DELete
   Function Deletes the output items of numeric data.
   Syntax :NUMeric[:NORMal]:DELete {<NRf>
         [,<NRf>]}
         1st <NRf> = 1 to 255 (Item number to start
         deleting)
         2nd <NRf> = 1 to 255 (Item number to end
         deleting)
   Example :NUMERIC:NORMAL:CLEAR 1 (Deletes
         ITEM1 and shift ITEM2 and subsequent
         items forward)
         :NUMERIC:NORMAL:CLEAR 1,3 (Deletes
         ITEM1 to ITEM3 and shift ITEM4 and subsequent
         items forward)
   Description • The subsequent output items fill the positions
          of deleted output items, and empty sections at
          the end are set to “NONE.”
         • If the 2nd <NRf> is omitted, only the output
          item of the delete start number is deleted.
```
### Right column
```text
                   6.18 NUMeric Group

 :NUMeric[:NORMal]:ITEM<x>
 Function Sets the numeric data output items (function,
       element, and harmonic order) or queries the
       current setting.
 Syntax :NUMeric[:NORMal]:ITEM<x> {NONE|
       <Function>,<Element>[,<Order>]}
       :NUMeric[:NORMal]:ITEM<x>?
       <x> = 1 to 255 (item number)
       NONE = No output item
       <Function> = {U|I|P|S|Q|...}(See the
       function selection list (1) of “DISPlay group” on
       page 6-44.)
       <Element> = {<NRf>|SIGMa|SIGMB} (<NRf>
       = 1 to 4)
       <Order> = {TOTal|DC|<NRf>} (<NRf> = 1 to
       100)
 Example :NUMERIC:NORMAL:ITEM1 U,1,TOTAL
       :NUMERIC:NORMAL:ITEM1? ->
       :NUMERIC:NORMAL:ITEM1 U,1,TOTAL
 Description • If <Element> is omitted, element 1 is set.
       • If <Order> is omitted, TOTal is set.
       • <Element> or <Order> is omitted from
        response to functions that do not need them.
 :NUMeric[:NORMal]:NUMber
 Function Sets the number of the numeric data that is
       transmitted by “:NUMeric[:NORMal]:VALue?” or
       queries the current setting.
 Syntax :NUMeric[:NORMal]:NUMber {<NRf>|ALL}
       :NUMeric[:NORMal]:NUMber?
       <NRf> = 1 to 255(ALL)
 Example :NUMERIC:NORMAL:NUMBER 15
       :NUMERIC:NORMAL:NUMBER ->
       :NUMERIC:NORMAL:NUMBER 15
 Description • If the parameter is omitted for the
        “:NUMeric[:NORMal]:VALue?” command,
        the numeric data from 1 to (the specified value)
        is output in order.
       • By default, the number of numeric data is set to
        “15.”
 :NUMeric[:NORMal]:PRESet
 Function Presets the output item pattern of numeric data.
 Syntax :NUMeric[:NORMal]:PRESet {<NRf>}
       <NRf> = 1 to 4
 Example :NUMERIC:NORMAL:PRESET 1
 Description • For details on the output items that are preset,
        see “(1) Preset Pattern of Numeric Data Output
        Items” (page 6-98).
       • By default, output items of “Pattern 2” is
        selected.
```

## Page 6-96

### Left column
```text
 6.18 NUMeric Group

 :NUMeric[:NORMal]:VALue?
 Function Queries the numeric data.
 Syntax :NUMeric[:NORMal]:VALue? {<NRf>}
       <NRf> = 1 to 255 (item number)
 Example • Example when <NRf> is specified
        :NUMERIC:NORMAL:VALUE? 1 ->
        104.75E+00
       • Example when <NRf> is omitted
        :NUMERIC:NORMAL:VALUE? ->
        104.75E+00,105.02E+00,
        -0.38E+00,..(omitted)..,49.868E+00
       • Example in which “:NUMeric:FORMat” is set
        to “FLOat”
        :NUMERIC:NORMAL:VALUE? -> #4(number
        of bytes, 4 digits)(data byte sequence)
 Description • If <NRf> is specified, only the numeric data of
        the item number is output.
       • If <NRf> is omitted, the numeric
        data of item numbers from 1 to
        “:NUMeric[:NORMal]:NUMber” is output in
        order.
       • For the format of the individual numeric data
        that is output, see “Numeric Data Format” at
        the end of this group of commands (see page
        6-97).
```

## Page 6-97

```text
                                                       6.18 NUMeric Group

     * Numeric Data Format
                 (1) Normal Data
                   • Frequency (FU and FI)
                    ASCII: <NR3> format (mantissa: 5 digits, exponent: 2 digits, example: 50.000E+00)
                    FLOAT: IEEE single-precision floating point (4-byte) format
                   • Elapsed time of integration (TIME)
                    ASCII: <NR1> format in units of seconds (example: for 1 hour (1:00:00), 3600)
                    FLOAT: IEEE single-precision floating point (4-byte) format in units of seconds
                    (example: for 1 hour (1:00:00), 0x45610000)
                   • Peak information (PKU, PKI, PKSPeed, PKTorque) for Cycle by Cycle measurement
                                         ASCII     FLOAT
                                         (<NR1> format) (IEEE single-precision floating
                                                   point (4-byte) format)
                    No peak “ ”:         “0”       0x00000000 (0)
                    Positive peak “↑+”:  “1”       0x3F800000 (1)
                    Negative peak “↓-”:  “2”       0x40000000 (2)
                    Positive and negative peak “ ↑↓ ±”: “3” 0x40400000 (3)

                   Note
                      If the main unit’s peak over detection function makes a detection during the measurement
                      period, 4 is added to the numbers above.

                   • No items (NONE)
                    ASCII: “NAN” (Not A Number)
                       FLOAT: 0x7E951BEE (9.91E+37)
                   • Other than above
                    ASCII: <NR3> format (mantissa: maximum significant digits = 6, exponent: 2 digits,
                    example: [-]123.456.45E+00)
                    FLOAT: IEEE single-precision floating point (4-byte) format

                 (2) Error Data
                    •  Data does not exist (display: “---------”)
                       ASCII: “NAN” (Not A Number)
                       FLOAT: 0x7E951BEE (9.91E+37)
                    •  Overrange (display: “---O L---”)
                    •  Overflow (display: “---O F---”)
                    •  Data over (display: “Error “)
                       ASCII: “INF” (INFinity)
                       FLOAT: 0x7E94F56A (9.9E+37)

                   Note
                    • For the 180° (Lead/Lag) display of the phase difference φ (PHI) of elements 1 to 4, the values
                      are output in the range between -180.000 to 180.000 with lead (D) and lag (G) set to negative
                      and positive values, respectively.
                    • For the Σ of power values (P, S, Q, and PC), the number of digits of the mantissa may be
                      equal to 7 (the maximum significant digits) depending on the combination of the voltage
                      range and current range (power range). See the list of power ranges in the User’s Manual IM
                      WT3001E-01EN.
```

## Page 6-98

```text
 6.18 NUMeric Group

                 * List of Numeric Data Output Items That Are Preset
                  The list of function names used in the commands and the corresponding function
                  names used on the screen menu of this instrument is given in the Function Selection
                  List in the DISPlay group.

                 Note
                    The List of Numeric Data Output Items That Are Preset indicates the measurement function
                    and element that are assigned to each item number (ITEM<x>). Items that are not set to be
                    measured are displayed or output in the same fashion as when the data does not exist. For
                    example, if frequency FI of the current of element 2 is not set to be measured, the output of
                    item number ITEM19 is the same as the output when the data does not exist (NAN for ASCII).

               (1) Preset Pattern of Numeric Data Output Items
                  Applicable command “:NUMeric[:NORMal]:PRESet”
                  • Pattern 1
                    ITEM<x>     <Function>, <Element>,  <Order>
                    1           U,          1,          TOTal
                    2           I,          1,          TOTal
                    3           P,          1,          TOTal
                    4           S,          1,          TOTal
                    5           Q,          1,          TOTal
                    6           LAMBda,     1,          TOTal
                    7           PHI,        1,          TOTal
                    8           FU,         1,          (TOTal)
                    9           FI,         1,          (TOTal)
                    10          NONE,
                    11 to 19    U to FI,    2,          TOTal
                    20          NONE,
                    21 to 29    U to FI,    3,          TOTal
                    30          NONE,
                    31 to 39    U to FI,    4,          TOTal
                    40          NONE,
                    41 to 49    U to FI,    SIGMA,      TOTal
                    50          NONE,
                    51 to 59    U to FI,    SIGMB,      TOTal
                    60          NONE,
                    61 to 255   NONE,

                 • Pattern 2
                    ITEM<x>     <Function>, <Element>,  <Order>
                    1           U,          1,          TOTal
                    2           I,          1,          TOTal
                    3           P,          1,          TOTal
                    4           S,          1,          TOTal
                    5           Q,          1,          TOTal
                    6           LAMBda,     1,          TOTal
                    7           PHI,        1,          TOTal
                    8           FU,         1,          (TOTal)
                    9           FI,         1,          (TOTal)
                    10          UPPeak,     1,          (TOTal)
                    11          UMPeak,     1,          (TOTal)
```

## Page 6-99

```text
                                                       6.18 NUMeric Group

                      12          IPPeak,     1,          (TOTal)
                      13          IMPeak,     1,          (TOTal)
                      14          CFU,        1,          (TOTal)
                      15          CFI,        1,          (TOTal)
                      16 to 30    U to CFI,   2,          TOTal
                      31 to 45    U to CFI,   3,          TOTal
                      46 to 60    U to CFI,   4,          TOTal
                      61 to 75    U to CFI,   SIGMA,      TOTal
                      76 to 90    U to CFI,   SIGMB,      TOTal
                      91 to 255   NONE,

                    • Pattern 3
                      ITEM<x>     <Function>, <Element>,  <Order>
                      1           U,          1,          TOTal
                      2           I,          1,          TOTal
                      3           P,          1,          TOTal
                      4           S,          1,          TOTal
                      5           Q,          1,          TOTal
                      6           TIME,       1,          (TOTal)
                      7           WH,         1,          (TOTal)
                      8           WHP,        1,          (TOTal)
                      9           WHM,        1,          (TOTal)
                      10          AH,         1,          (TOTal)
                      11          AHP,        1,          (TOTal)
                      12          AHM,        1,          (TOTal)
                      13          WS,         1,          (TOTal)
                      14          WQ,         1,          (TOTal)
                      15          NONE,
                      16 to 29    U to WQ,    2,          TOTal
                      30          NONE,
                      31 to 44    U to WQ,    3,          TOTal
                      45          NONE,
                      46 to 59    U to WQ,    4,          TOTal
                      60          NONE,
                      61 to 74    U to WQ,    SIGMA,      TOTal
                      75          NONE,
                      76 to 89    U to WQ,    SIGMB,      TOTal
                      90          NONE,
                      91 to 255   NONE,

                    • Pattern 4
                      ITEM<x>     <Function>, <Element>,  <Order>
                      1           U,          1,          TOTal
                      2           I,          1,          TOTal
                      3           P,          1,          TOTal
                      4           S,          1,          TOTal
                      5           Q,          1,          TOTal
                      6           LAMBda,     1,          TOTal
                      7           PHI,        1,          TOTal
                      8           FU,         1,          (TOTal)
```

## Page 6-100

```text
 6.18 NUMeric Group

                    9           FI,         1,          (TOTal)
                    10          UPPeak,     1,          (TOTal)
                    11          UMPeak,     1,          (TOTal)
                    12          IPPeak,     1,          (TOTal)
                    13          IMPeak,     1,          (TOTal)
                    14          CFU,        1,          (TOTal)
                    15          CFI,        1,          (TOTal)
                    16          PC,         1,          (TOTal)
                    17          TIME,       1,          (TOTal)
                    18          WH,         1,          (TOTal)
                    19          WHP,        1,          (TOTal)
                    20          WHM,        1,          (TOTal)
                    21          AH,         1,          (TOTal)
                    22          AHP,        1,          (TOTal)
                    23          AHM,        1,          (TOTal)
                    24          WS,         1,          (TOTal)
                    25          WQ,         1,          (TOTal)
                    26 to 50    U to WQ,    2,          TOTal
                    51 to 75    U to WQ,    3,          TOTal
                    76 to 100   U to WQ,    4,          TOTal
                    101 to 125  U to WQ,    SIGMA,      TOTal
                    126 to 150  U to WQ,    SIGMB,      TOTal
                    151 to 255  NONE,

               (2) Preset Pattern of the Numeric List Data Output Items of Harmonic
                  Measurement
                  Applicable command “:NUMeric:LIST:PRESet”
                  • Pattern 1
                    ITEM<x>     <Function>, <Element>
                    1           U,          1
                    2           I,          1
                    3           P,          1
                    4 to 6      U to P,     2
                    7 to 9      U to P,     3
                    10 to 12    U to P,     4
                    13 to 64    NONE,

                 • Pattern 2
                    ITEM<x>     <Function>, <Element>
                    1           U,          1
                    2           I,          1
                    3           P,          1
                    4           PHIU,       1
                    5           PHII,       1
                    6 to 10     U to PHII,  2
                    11 to 15    U to PHII,  3
                    16 to 20    U to PHII,  4
                    21 to 64    NONE,
```

## Page 6-101

```text
                                                       6.18 NUMeric Group

                    • Pattern 3
                      ITEM<x>     <Function>, <Element>
                      1           U,          1
                      2           I,          1
                      3           P,          1
                      4           Q,          1
                      5           Z,          1
                      6           RS,         1
                      7           XS,         1
                      8           RP,         1
                      9           XP,         1
                      10 to 18    U to XP,    2
                      19 to 27    U to XP,    3
                      28 to 36    U to XP,    4
                      37 to 64    NONE,

                    • Pattern 4
                      ITEM<x>     <Function>, <Element>
                      1           U,          1
                      2           I,          1
                      3           P,          1
                      4           S,          1
                      5           Q,          1
                      6           LAMBda,     1
                      7           PHI,        1
                      8           PHIU,       1
                      9           PHII,       1
                      10          Z,          1
                      11          RS,         1
                      12          XS,         1
                      13          RP,         1
                      14          XP,         1
                      15 to 28    U to XP,    2
                      29 to 42    U to XP,    3
                      43 to 56    U to XP,    4
                      57 to 64    NONE,
```

## Page 6-102

### Section introduction
```text
   6.19   RATE   Group

 The commands in this group deal with the data update interval.
 You can make the same settings and inquiries as when UPDATE RATE on the front panel is used.
```
### Left column
```text
 :RATE
 Function Sets the data update interval or queries the
       current setting.
 Syntax :RATE {<Time>}
       :RATE?
       <Time> = 50, 100, 250, 500 (ms), 1, 2, 5, 10, or
       20 (s)
 Example :RATE 500MS
       :RATE? -> :RATE 500.0E-03
```

## Page 6-103

### Section introduction
```text
     6.20   STATus    Group

   The commands in the STATus group are used to make settings and inquiries related to the status report. There are
   no front panel keys that correspond to the commands in this group. For details on the status report, see chapter 7.
```
### Left column
```text
   :STATus?
   Function Queries all settings related to the communication
         status function.
   Syntax :STATus?
   Example :STATUS? -> :STATUS:EESE 0;
         FILTER1 NEVER;FILTER2 NEVER;
         FILTER3 NEVER;FILTER4 NEVER;
         FILTER5 NEVER;FILTER6 NEVER;
         FILTER7 NEVER;FILTER8 NEVER;
         FILTER9 NEVER;FILTER10 NEVER;
         FILTER11 NEVER;FILTER12 NEVER;
         FILTER13 NEVER;FILTER14 NEVER;
         FILTER15 NEVER;FILTER16 NEVER;
         QENABLE 1;QMESSAGE 1
   :STATus:CONDition?
   Function Queries the contents of the condition register.
   Syntax :STATus:CONDition?
   Example :STATUS:CONDITION? -> 16
   Description For details on the condition register, see chapter 7,
         “Status Report.”

   :STATus:EESE(Extended Event Status
   Enable register)
   Function Sets the extended event enable register or
         queries the current setting.
   Syntax :STATus:EESE <Register>
         :STATus:EESE?
         <Register> = 0 to 65535
   Example :STATUS:EESE #B0000000000000000
         :STATUS:EESE? -> :STATUS:EESE 0
   Description For details on the extended event enable register,
         see chapter 7, “Status Report.”
   :STATus:EESR?(Extended Event Status
   Register)
   Function Queries the content of the extended event
         register and clears the register.
   Syntax :STATus:EESR?
   Example :STATUS:EESR? -> 0
   Description For details on the extended event register, see
         chapter 7, “Status Report.”
```
### Right column
```text
 :STATus:ERRor?
 Function Queries the error code and message information
       (top of the error queue).
 Syntax :STATus:ERRor?
 Example :STATUS:ERROR? ->
       113,”Underfined Header”
 Description • When there is no error, “0, “No error”” is
         returned.
       • The message cannot be returned in Japanese.
       • You can specify whether to add the message
         using the “STATus:QMESsage” command.
 :STATus:FILTer<x>
 Function Sets the transition filter or queries the current
       setting.
 Syntax :STATus:FILTer<x> {RISE|FALL|BOTH|
       NEVer}
       :STATus:FILTer<x>?
       <x> = 1 to 16
 Example :STATUS:FILTER2 RISE
       :STATUS:FILTER2? -> :STATUS:FILTER2
       RISE
 Description • Specify how each bit of the condition register
         is to change to set the event. If “RISE” is
         specified, the event is set when the bit changes
         from 0 to 1.
       • For details on the transition, see chapter 7,
         “Status Report.”
 :STATus:QENable
 Function Sets whether to store messages other than
       errors to the error queue (ON/OFF) or queries the
       current setting.
 Syntax :STATus:QENable {<Boolean>}
       :STATus:QENable?
 Example :STATUS:QENABLE ON
       :STATUS:QENABLE? ->
       :STATUS:QENABLE 1
 :STATus:QMESsage
 Function Sets whether to attach message information to
       the response to the “STATus:ERRor?” query (ON/
       OFF) or queries the current setting.
 Syntax :STATus:QMESsage {<Boolean>}
       :STATus:QMESsage?
 Example :STATUS:QMESSAGE ON
       :STATUS:QMESSAGE? ->
       :STATUS:QMESSAGE 1
```

## Page 6-104

### Left column
```text
 6.20 STATus Group

 :STATus:SPOLl? (Serial Poll)
 Function Executes serial polling.
 Syntax :STATus:SPOLl?
 Example :STATUS:SPOLL? -> :STATUS:SPOLL 0
 Description This command is dedicated to the optional RS-
       232, USB, or Ethernet interface. An interface
       message is available for the GP-IB interface.
```

## Page 6-105

### Section introduction
```text
     6.21   STORe    Group

   The commands in this group deal with store and recall.
   You can make the same settings and inquiries as when STORE and STORE SET (SHIFT+STORE) on the front panel
   is used.
```
### Left column
```text
   :STORe?
   Function Queries all settings related to store and recall.
   Syntax :STORe?
   Example :STORE? -> STORE:MODE STORE;
         DIRECTION MEMORY;SMODE MANUAL;
         COUNT 100;INTERVAL 0,0,0;
         ITEM NUMERIC;NUMERIC:NORMAL:
         ELEMENT1 1;ELEMENT2 0;ELEMENT3 0;
         ELEMENT4 0;SIGMA 0;SIGMB 0;U 1;I 1;
         P 1;S 1;Q 1;LAMBDA 1;PHI 1;FU 1;
         FI 1;UPPEAK 0;UMPEAK 0;IPPEAK 0;
         IMPEAK 0;CFU 0;CFI 0;PC 0;TIME 0;
         WH 0;WHP 0;WHM 0;AH 0;AHP 0;AHM 0;
         WS 0;WQ 0;ETA1 0;ETA2 0;ETA3 0;
         ETA4 0;F1 0;F2 0;F3 0;F4 0;F5 0;
         F6 0;F7 0;F8 0;F9 0;F10 0;F11 0;
         F12 0;F13 0;F14 0;F15 0;F16 0;
         F17 0;F18 0;F19 0;F20 0;:STORE:
         MEMORY:ALERT 1
   :STORe:COUNt
   Function Sets the store count or queries the current
         setting.
   Syntax :STORe:COUNt {<NRf>}
         :STORe:COUNt?
         <NRf> = 1 to 999999
   Example :STORE:COUNT 100
         :STORE:COUNT? -> :STORE:COUNT 100
   :STORe:DIRection
   Function Sets the store destination or queries the current
         setting.
   Syntax :STORe:DIRection {MEMory|FILE}
         :STORe:DIRection?
   Example :STORE:DIRECTION MEMORY
         :STORE:DIRECTION? -> :STORE:DIRECTION
         MEMORY
   :STORe:FILE?
   Function Queries all settings related to the saving of the
         stored data.
   Syntax :STORe:FILE?
   Example :STORE:FILE? -> :STORE:FILE:
         TYPE ASCII;ANAMING 1;NAME “DATA1”;
         COMMENT “CASE1”
```
### Right column
```text
 :STORe:FILE:ANAMing
 Function Sets whether to automatically name the files
       when saving the stored data or queries the
       current setting.
 Syntax :STORe:FILE:ANAMing {<Boolean>}
       :STORe:FILE:ANAMing?
 Example :STORE:FILE:ANAMING ON
       :STORE:FILE:ANAMING? ->
       :STORE:FILE:ANAMING 1
 :STORe:FILE:COMMent
 Function Sets the comment to be added to the file when
       saving the stored data or queries the current
       setting.
 Syntax :STORe:FILE:COMMent {<String>}
       :STORe:FILE:COMMent?
       <String> = Up to 25 characters
 Example :STORE:FILE:COMMENT “CASE1”
       :STORE:FILE:COMMENT? ->
       :STORE:FILE:COMMENT “CASE1”

 :STORe:FILE:NAME
 Function Sets the name of the file when saving the stored
       data or queries the current setting.
 Syntax :STORe:FILE:NAME {<Filename>}
       :STORe:FILE:NAME?
 Example :STORE:FILE:NAME “DATA1”
       :STORE:FILE:NAME? -> :STORE:FILE:NAME
       “DATA1”
 Description Set the save destination drive and directory of the
       stored data using the following commands.
       • Destination drive: “:FILE:DRIVe”
       • Directory: “:FILE:CDIRectory”
       The save destination path can be queried using
       the “:FILE:PATH?” command.
 :STORe:FILE:TYPE
 Function Sets the data format when saving the stored data
       or queries the current setting.
 Syntax :STORe:FILE:TYPE {ASCii|FLOat}
       :STORe:FILE:TYPE?
 Example :STORE:FILE:TYPE ASCII
       :STORE:FILE:TYPE? -> :STORE:FILE:TYPE
       ASCII
```

## Page 6-106

### Left column
```text
 6.21 STORe Group

 :STORe:INTerval
 Function Sets the store interval or queries the current
       setting.
 Syntax :STORe:INTerval {<NRf>,<NRf>,<NRf>}
       :STORe:INTerval?
       1st <NRf> = 0 to 99 (hour)
       2nd <NRf> = 0 to 59 (minute)
       3rd <NRf> = 1 to 59 (second)
 Example :STORE:INTERVAL 0,0,0
       :STORE:INTERVAL? ->
       :STORE:INTERVAL 0,0,0
 :STORe:ITEM
 Function Sets the stored item or queries the current
       setting.
 Syntax :STORe:ITEM {NUMeric|WAVE|NWAVe}
       :STORe:ITEM?
       NUMeric = Store only the numeric data.
       WAVE = Store only the waveform display data
       NWAVe = Store both the numeric data and
       waveform display data
 Example :STORE:ITEM NUMERIC
       :STORE:ITEM? -> :STORE:ITEM NUMERIC
 :STORe:MEMory?
 Function Queries all settings related to the storage
       memory.
 Syntax :STORe:MEMory?
 Example :STORE:MEMORY? ->
       :STORE:MEMORY:ALERT 1

 :STORe:MEMory:ALERt
 Function Sets whether to display a confirmation message
       when clearing the storage memory or queries the
       current setting.
 Syntax :STORe:MEMory:ALERt {<Boolean>}
       :STORe:MEMory:ALERt?
 Example :STORE:MEMORY:ALERT ON
       :STORE:MEMORY:ALERT? ->
       :STORE:MEMORY:ALERT 1
 Description The initialization takes place immediately
       when initializing the storage memory using the
       “:STORe:MEMory:INITialize” command
       regardless of the setting specified with this
       command.
 :STORe:MEMory:CONVert:ABORt
 Function Abort converting the stored data from the memory
       to the file.
 Syntax :STORe:MEMory:CONVert:ABORt
 Example :STORE:MEMORY:CONVERT:ABORT
```
### Right column
```text
 :STORe:MEMory:CONVert:EXECute
 Function Executes the converting of the stored data from
       the memory to the file.
 Syntax :STORe:MEMory:CONVert:EXECute
 Example :STORE:MEMORY:CONVERT:EXECUTE
 Description • The convert destination file is set using the
        “:STORe:FILE:...” command.
       • When file conversion is executed, this
        instrument accesses the file twice.
        To confirm the completion of the file conversion,
        use the “COMMUNICATE:WAIT 64” command
        (checks the change in bit 6 (ACS) of the
        condition register) and check the completion
        of the file access of this instrument twice. An
        example is indicated below.
          “STATUS:EESR?”
        (Clear the extended event register)
          “STORE:MEMORY:CONVERT:EXECUTE”
        (Start the file conversion)
          “COMMUNICATE:WAIT 64”
        (Wait for the conversion to finish, the first time)
          “STATUS:EESR?”
        (Clear the extended event register)
          “COMMUNICATE:WAIT 64”
        (Wait for the conversion to finish, the second
        time)
          “STATUS:EESR?”
        (Clear the extended event register)
 :STORe:MEMory:INITialize
 Function Executes the initialization of the storage memory.
 Syntax :STORe:MEMory:INITialize
 Example :STORE:MEMORY:INITIALIZE
 :STORe:MODE
 Function Sets the data storage/recall or queries the current
       setting.
 Syntax :STORe:MODE {STORe|RECall}
       :STORe:MODE?
 Example :STORE:MODE STORE
       :STORE:MODE? -> :STORE:MODE STORE
```

## Page 6-107

### Left column
```text
   :STORe:NUMeric?
   Function Queries all settings related to the storage of
         numeric data.
   Syntax :STORe:NUMeric?
   Example :STORE:NUMERIC? -> :STORE:NUMERIC:
         NORMAL:ELEMENT1 1;ELEMENT2 0;
         ELEMENT3 0;ELEMENT4 0;SIGMA 0;
         SIGMB 0;U 1;I 1;P 1;S 1;Q 1;
         LAMBDA 1;PHI 1;FU 1;FI 1;UPPEAK 0;
         UMPEAK 0;IPPEAK 0;IMPEAK 0;CFU 0;
         CFI 0;PC 0;TIME 0;WH 0;WHP 0;WHM 0;
         AH 0;AHP 0;AHM 0;WS 0;WQ 0;ETA1 0;
         ETA2 0;ETA3 0;ETA4 0;F1 0;F2 0;
         F3 0;F4 0;F5 0;F6 0;F7 0;F8 0;F9 0;
         F10 0;F11 0;F12 0;F13 0;F14 0;
         F15 0;F16 0;F17 0;F18 0;F19 0;F20 0
   :STORe:NUMeric:NORMal?
   Function Queries all settings related to the stored items of
         numeric data.
   Syntax :STORe:NUMeric:NORMal?
   Example :STORE:NUMERIC:NORMAL? ->
         :STORE:NUMERIC:NORMAL:ELEMENT1 1;
         ELEMENT2 0;ELEMENT3 0;ELEMENT4 0;
         SIGMA 0;SIGMB 0;U 1;I 1;P 1;S 1;
         Q 1;LAMBDA 1;PHI 1;FU 1;FI 1;
         UPPEAK 0;UMPEAK 0;IPPEAK 0;
         IMPEAK 0;CFU 0;CFI 0;PC 0;TIME 0;
         WH 0;WHP 0;WHM 0;AH 0;AHP 0;AHM 0;
         WS 0;WQ 0;ETA1 0;ETA2 0;ETA3 0;
         ETA4 0;F1 0;F2 0;F3 0;F4 0;F5 0;
         F6 0;F7 0;F8 0;F9 0;F10 0;F11 0;
         F12 0;F13 0;F14 0;F15 0;F16 0;
         F17 0;F18 0;F19 0;F20 0
   :STORe:NUMeric[:NORMal]:ALL
   Function Collectively turns ON/OFF the output of all
         element functions when storing the numerical
         data.
   Syntax :STORe:NUMeric[:NORMal]:
         ALL {<Boolean>}
   Example :STORE:NUMERIC[:NORMAL]:ALL ON
```
### Right column
```text
                    6.21 STORe Group

 :STORe:NUMeric[:NORMal]:{ELEMent<x>|
 SIGMA|SIGMB}
 Function Turns ON/OFF the output of {each
       element|ΣA|ΣB} when storing the numeric data.
 Syntax :STORe:NUMeric[:NORMal]:
       {ELEMent<x>|SIGMA|SIGMB} {<Boolean>}
       :STORe:NUMeric[:NORMal]:
       {ELEMent<x>|SIGMA|SIGMB}?
       <x> = 1 to 4
 Example :STORE:NUMERIC:NORMAL:ELEMENT1 ON
       :STORE:NUMERIC:NORMAL:ELEMENT1? ->
       :STORE:NUMERIC:NORMAL:ELEMENT1 1
 Description • :STORe:NUMeric[:NORMal]:SIGMA is
        valid on models with two or more elements.
        To turn the output ON, wiring unit ΣA must exist
        by setting the wiring system beforehand using
        the [:INPut]WIRing command.
       • :STORe:NUMeric[:NORMal]:SIGMB is
        valid on models with four elements. To turn
        the output ON, wiring unit ΣB must exist by
        setting the wiring system beforehand using the
        [:INPut]WIRing command.
 :STORe:NUMeric[:NORMal]:PRESet<x>
 Function Presets the output ON/OFF pattern of the
       element function for storing the numeric data.
 Syntax :STORe:NUMeric[:NORMal]:PRESet<x>
       <x> = 1 to 2 (preset pattern number)
 Example :STORE:NUMERIC:NORMAL:PRESET1
 Description For details on the storage pattern when preset is
       executed, see the User’s Manual IM WT3001E-
       01EN.
 :STORe:NUMeric[:NORMal]:<Function>
 Function Turns ON/OFF the output of the function when
       storing the numerical data or queries the current
       setting.
 Syntax :STORe:NUMeric[:NORMal]:<Function>
       {<Boolean>}
       :STORe:NUMeric[:NORMal]:<Function>?
       <Function> = {U|I|P|S|Q|...}(See the
       function selection list (1) of “DISPlay group” on
       page 6-44.)
 Example :STORE:NUMERIC:NORMAL:U ON
       :STORE:NUMERIC:NORMAL:U? ->
       :STORE:NUMERIC:NORMAL:U 1
```

## Page 6-108

### Left column
```text
 6.21 STORe Group

 :STORe:RECall
 Function Sets the data number to be recalled or queries
       the current setting.
 Syntax :STORe:RECall {<NRf>}
       :STORe:RECall?
       <NRf> = 1 to 999999
 Example :STORE:RECALL 1
       :STORE:RECALL? -> :STORE:RECALL 1
 :STORe:RTIMe?
 Function Queries the store reservation time for real-time
       store mode.
 Syntax :STORe:RTIMe?
 Example :STORE:RTIME? -> :STORE:RTIME:
       START 2005,1,1,0,0,0;
       END 2005,1,1,1,0,0

 :STORe:RTIMe:{STARt|END}
 Function Sets the store {start|stop} reservation date/time
       for real-time store mode or queries the current
       setting.
 Syntax :STORe:RTIMe:{STARt|END} {<NRf>,
       <NRf>,<NRf>,<NRf>,<NRf>,<NRf>}
       :STORe:RTIMe:{STARt|END}?
       {<NRf>, <NRf>, <NRf>, <NRf>, <NRf>, <NRf>} =
       2001, 1, 1, 0, 0, 0 to 2099, 12, 31, 23, 59, 59
       1st <NRf> = 2001 to 2099 (year)
       2nd <NRf> = 1 to 12 (month)
       3rd <NRf> = 1 to 31 (day)
       4th <NRf> = 0 to 23 (hour)
       5th <NRf> = 0 to 59 (minute)
       6th <NRf> = 0 to 59 (second)
 Example :STORE:RTIME:START 2005,1,1,0,0,0
       :STORE:RTIME:START? ->
       :STORE:RTIME:START 2005,1,1,0,0,0
 Description This command is valid when the store mode
       (:STORe:SMODe) is set to RTIMe (real-time
       store mode).
 :STORe:SMODe
 Function Sets the store mode or queries the current
       setting.
 Syntax :STORe:SMODe {MANual|RTIMe|
       INTEGrate}
       :STORe:SMODe?
       MANual = Manual store mode
       RTIMe = Real-time store mode
       INTEGrate = Integration synchronization store
       mode
 Example :STORE:SMODE MANUAL
       :STORE:SMODE? ->
       :STORE:SMODE MANUAL
```
### Right column
```text
 :STORe:STARt
 Function Starts the data store operation.
 Syntax :STORe:STARt
 Example :STORE:START
 Description When “:STORe:SMODe” is set to MANual, the
       storage operation is executed. When set to
       {RTIMe|INTEGrate} this instrument enters the
       store wait state.
 :STORe:STOP
 Function Stops the data storage operation.
 Syntax :STORe:STOP
 Example :STORE:STOP

 :STORe:WAVE?
 Function Queries all settings related to the storage of
       waveform display data.
 Syntax :STORe:WAVE?
 Example :STORE:WAVE? -> :STORE:WAVE:U1 1;
       U2 0;U3 0;U4 0;I1 1;I2 0;I3 0;I4 0
 :STORe:WAVE:ALL
 Function Collectively turns ON/OFF the output of all
       waveforms when storing waveform display data.
 Syntax :STORe:WAVE:ALL {<Boolean>}
 Example :STORE:WAVE:ALL ON

 :STORe:WAVE:{U<x>|I<x>|SPEed|TORQue}
 Function Turns ON/OFF the output of the waveform when
       storing the waveform display data or queries the
       current setting.
 Syntax :STORe:WAVE:{U<x>|I<x>|SPEed|
       TORQue} {<Boolean>}
       :STORe:WAVE:{U<x>|I<x>|SPEed|
       TORQue}?
       <x> = 1 to 4
 Example :STORE:WAVE:U1 ON
       :STORE:WAVE:U1? -> :STORE:WAVE:U1 1
 Description {SPEed|TORQue} are valid only on models with
       the motor evaluation function (/MTR option).
```

## Page 6-109

### Section introduction
```text
     6.22   SYSTem     Group

   The commands in this group deal with the system.
   You can make the same settings and inquiries as when MISC on the front panel is used.
```
### Left column
```text
   :SYSTem?
   Function Queries all settings related to the system.
   Syntax :SYSTem?
   Example :SYSTEM? -> :SYSTEM:LANGUAGE:
         MESSAGE ENGLISH;MENU ENGLISH;:
         SYSTEM:FONT GOTHIC;KLOCK 0;SLOCK 0;
         LCD:BRIGHTNESS 2;COLOR:GRAPH:
         MODE DEFAULT;:SYSTEM:LCD:COLOR:
         TEXT:MODE PRESET1

   :SYSTem:CLOCk?
   Function Sets all date/time related settings or queries the
         current setting.
   Syntax :SYSTem:CLOCk?
   Example :SYSTEM:CLOCK? ->
         :SYSTEM:CLOCK:DISPLAY 1;TYPE MANUAL
   :SYSTem:CLOCk:DISPlay
   Function Turns ON/OFF the date/time display or queries
         the current setting.
   Syntax :SYSTem:CLOCk:DISPlay {<Boolean>}
         :SYSTem:CLOCk:DISPlay?
   Example :SYSTEM:CLOCK:DISPLAY ON
         :SYSTEM:CLOCK:DISPLAY? ->
         :SYSTEM:CLOCK:DISPLAY 1
   :SYSTem:CLOCk:SNTP?
   Function Sets all SNTP-based date/time related settings or
         queries the current setting.
   Syntax :SYSTem:CLOCk:SNTP?
   Example :SYSTEM:CLOCK:SNTP? ->
         :SYSTEM:CLOCK:SNTP:GMTTIME “09:00”
   Description Available only with Ethernet (/C7 option).

   :SYSTem:CLOCk:SNTP[:EXECute]
   Function Sets the date/time via SNTP.
   Syntax :SYSTem:CLOCk:SNTP[:EXECute]
   Example :SYSTEM:CLOCK:SNTP:EXECUTE
   Description Available only with Ethernet (/C7 option).
```
### Right column
```text
 :SYSTem:CLOCk:SNTP:GMTTime
 Function Sets the difference from Greenwich Mean Time
       or queries the current setting.
 Syntax :SYSTem:CLOCk:SNTP:GMTTime {<string>}
       :SYSTem:CLOCk:SNTP:GMTTime?
       <string> = “HH:MM” (HH = hours, MM = minutes)
 Example :SYSTEM:CLOCK:SNTP:GMTTIME “09:00”
       :SYSTEM:CLOCK:SNTP:GMTTIME? ->
       :SYSTEM:CLOCK:SNTP:GMTTIME “09:00”
 Description • Available only with Ethernet (/C7 option).
       • Available when the date/time setting method
        (:SYSTem:CLOCk:TYPE) is SNTP.
 :SYSTem:CLOCk:TYPE
 Function Sets the date/time setting method or queries the
       current setting.
 Syntax :SYSTem:CLOCk:TYPE {MANual|SNTP}
       :SYSTem:CLOCk:TYPE?
 Example :SYSTEM:CLOCK:TYPE MANUAL
       :SYSTEM:CLOCK:TYPE? ->
       :SYSTEM:CLOCK:TYPE MANUAL
 Description SNTP is available only with Ethernet (/C7 option).
 :SYSTem:DATE
 Function Sets the date or queries the current setting.
 Syntax :SYSTem:DATE {<String>}
       :SYSTem:DATE?
       <String> = “YY/MM/DD” (YY = year, MM = month,
       DD = day)
 Example :SYSTEM:DATE “05/01/01”
       :SYSTEM:DATE? -> “05/01/01”
 Description “Year” is the lowest two digits of the year.

 :SYSTem:ECLear
 Function Clears the error message displayed on the
       screen.
 Syntax :SYSTem:ECLear
 Example :SYSTEM:ECLEAR
 :SYSTem:FONT
 Function Sets the display font or queries the current
       setting.
 Syntax :SYSTem:FONT {GOTHic|ROMan}
       :SYSTem:FONT?
 Example :SYSTEM:FONT GOTHIC
       :SYSTEM:FONT? ->
       :SYSTEM:FONT GOTHIC
```

## Page 6-110

### Left column
```text
 6.22 SYSTem Group

 :SYSTem:KLOCk
 Function Turns ON/OFF the key lock or queries the current
       setting.
 Syntax :SYSTem:KLOCk {<Boolean>}
       :SYSTem:KLOCk?
 Example :SYSTEM:KLOCK OFF
       :SYSTEM:KLOCK? -> :SYSTEM:KLOCK 0
 :SYSTem:LANGuage?
 Function Queries all settings related to the display
       language.
 Syntax :SYSTem:LANGuage?
 Example :SYSTEM:LANGUAGE? ->
       :SYSTEM:LANGUAGE:MESSAGE ENGLISH;
       MENU ENGLISH

 :SYSTem:LANGuage:MENU
 Function Sets the menu language or queries the current
       setting.
 Syntax :SYSTem:LANGuage:MENU {JAPANese|
       ENGLish}
       :SYSTem:LANGuage:MENU?
 Example :SYSTEM:LANGUAGE:MENU ENGLISH
       :SYSTEM:LANGUAGE:MENU? ->
       :SYSTEM:LANGUAGE:MENU ENGLISH
 :SYSTem:LANGuage:MESSage
 Function Sets the message language or queries the
       current setting.
 Syntax :SYSTem:LANGuage:MESSage {JAPANese|
       ENGLish}
       :SYSTem:LANGuage:MESSage?
 Example :SYSTEM:LANGUAGE:MESSAGE ENGLISH
       :SYSTEM:LANGUAGE:MESSAGE? ->
       :SYSTEM:LANGUAGE:MESSAGE ENGLISH
 :SYSTem:LCD?
 Function Queries all settings related to the LCD monitor.
 Syntax :SYSTem:LCD?
 Example :SYSTEM:LCD? ->
       :SYSTEM:LCD:BRIGHTNESS 2;COLOR:
       GRAPH:MODE DEFAULT;:SYSTEM:LCD:
       COLOR:TEXT:MODE PRESET1

 :SYSTem:LCD:BRIGhtness
 Function Sets the brightness of the LCD monitor or queries
       the current setting.
 Syntax :SYSTem:LCD:BRIGhtness {<NRf>}
       :SYSTem:LCD:BRIGhtness?
       <NRf> = –1 to 3
 Example :SYSTEM:LCD:BRIGHTNESS 2
       :SYSTEM:LCD:BRIGHTNESS? ->
       :SYSTEM:LCD:BRIGHTNESS 2
```
### Right column
```text
 :SYSTem:LCD:COLor?
 Function Queries all settings related to the display colors
       of the LCD monitor.
 Syntax :SYSTem:LCD:COLor?
 Example :SYSTEM:LCD:COLOR? -> :SYSTEM:LCD:
       COLOR:GRAPH:MODE DEFAULT;:SYSTEM:
       LCD:COLOR:TEXT:MODE PRESET1
 :SYSTem:LCD:COLor:GRAPh?
 Function Queries all settings related to the display colors
       of the graphic items.
 Syntax :SYSTem:LCD:COLor:GRAPh?
 Example :SYSTEM:LCD:COLOR:GRAPH? ->
       :SYSTEM:LCD:COLOR:GRAPH:MODE USER;
       BACKGROUND 0,0,0;GRATICULE 6,6,6;
       CURSOR 7,7,7;U1 7,7,0;U2 7,0,7;
       U3 7,0,0;U4 0,4,7;I1 0,7,0;
       I2 0,7,7;I3 7,4,0;I4 5,5,5

 :SYSTem:LCD:COLor:GRAPh:{BACKground|
 GRATicule|CURSor|U<x>|I<x>}
 Function Sets the display color of the {background|graticu
       le|cursor|voltage waveform|current waveform} or
       queries the current setting.
 Syntax :SYSTem:LCD:COLor:GRAPh:
       {BACKground|GRATicule|CURSor|U<x>|
       I<x>} {<NRf>,<NRf>,<NRf>}
       :SYSTem:LCD:COLor:GRAPh:
       {BACKground|GRATicule|CURSor|U<x>|
       I<x>}?
       <x> = 1 to 4
       <NRf> = 0 to 7
 Example :SYSTEM:LCD:COLOR:GRAPH:
       BACKGROUND 0,0,0
       :SYSTEM:LCD:COLOR:GRAPH:BACKGROUND?
       -> :SYSTEM:LCD:COLOR:GRAPH:
       BACKGROUND 0,0,0
 Description Set the color in the order R, G, and B.
       This command is valid when the
       display color mode of graphic items
       (:SYSTem:LCD:COLor:GRAPh:MODE) is set to
       “USER.”
 :SYSTem:LCD:COLor:GRAPh:MODE
 Function Sets the display color mode of the graphic items
       or queries the current setting.
 Syntax :SYSTem:LCD:COLor:GRAPh:
       MODE {DEFault|USER}
       :SYSTem:LCD:COLor:GRAPh:MODE?
 Example :SYSTEM:LCD:COLOR:GRAPH:
       MODE DEFAULT
       :SYSTEM:LCD:COLOR:GRAPH:MODE? ->
       :SYSTEM:LCD:COLOR:GRAPH:
       MODE DEFAULT
```

## Page 6-111

### Left column
```text
   :SYSTem:LCD:COLor:TEXT?
   Function Queries all settings related to the display colors
         of the text items.
   Syntax :SYSTem:LCD:COLor:TEXT?
   Example :SYSTEM:LCD:COLOR:TEXT? ->
         :SYSTEM:LCD:COLOR:TEXT:MODE USER;
         LETTER 7,7,7;BACKGROUND 2,2,6;
         BOX 0,0,7;SUB 3,3,3;SELECTED 0,4,7
   :SYSTem:LCD:COLor:TEXT:{LETTer|BACKg
   round|BOX|SUB|SELected}
   Function Sets the display color of the {text (Menu
         Fore)|menu background (Menu Back)|selected
         menu (Select Box)|pop-up menu (Sub
         Menu)|selected key (Selected Key)} or queries
         the current setting.
   Syntax :SYSTem:LCD:COLor:TEXT:{LETTer|
         BACKground|BOX|SUB|SELected} {<
         NRf>,<NRf>,<NRf>}
         :SYSTem:LCD:COLor:TEXT:{LETTer|
         BACKground|BOX|SUB|SELected}?
         <NRf> = 0 to 7
   Example :SYSTEM:LCD:COLOR:TEXT:LETTER 7,7,7
         :SYSTEM:LCD:COLOR:TEXT:LETTER? ->
         :SYSTEM:LCD:COLOR:TEXT:LETTER 7,7,7
   Description Set the color in the order R, G, and B.
         This command is valid when the
         display color mode of text items
         (:SYSTem:LCD:COLor:TEXT:MODE) is set to
         “USER.”
   :SYSTem:LCD:COLor:TEXT:MODE
   Function Sets the display color mode of the text items or
         queries the current setting.
   Syntax :SYSTem:LCD:COLor:TEXT:
         MODE {PRESet<x>|USER}
         :SYSTem:LCD:COLor:TEXT:MODE?
         <x> = 1 to 3
   Example :SYSTEM:LCD:COLOR:TEXT:MODE PRESET1
         :SYSTEM:LCD:COLOR:TEXT:MODE? ->
         :SYSTEM:LCD:COLOR:TEXT:MODE PRESET1
   :SYSTem:SLOCk
   Function Sets whether to continue the SHIFT key ON state
         or queries the current setting.
   Syntax :SYSTem:SLOCk {<Boolean>}
         :SYSTem:SLOCk?
   Example :SYSTEM:SLOCK OFF
         :SYSTEM:SLOCK? -> :SYSTEM:SLOCK 0
```
### Right column
```text
                   6.22 SYSTem Group

 :SYSTem:TIME
 Function Sets the time or queries the current setting.
 Syntax :SYSTem:TIME {<String>}
       :SYSTem:TIME?
       <String> = “HH:MM:SS” (HH = hour, MM =
       minute, SS = second)
 Example :SYSTEM:TIME “14:30:00”
       :SYSTEM:TIME? -> “14:30:00”
 :SYSTem:USBKeyboard
 Function Sets the USB keyboard type (language) or
       queries the current setting.
 Syntax :SYSTem:USBKeyboard {JAPANese|
       ENGLish}
       :SYSTem:USBKeyboard?
 Example :SYSTEM:USBKEYBOARD JAPANESE
       :SYSTEM:USBKEYBOARD? ->
       :SYSTEM:USBKEYBOARD JAPANESE
 Description This command is valid only on models with the
       USB port (peripheral device) (/C5 option).
```

## Page 6-112

### Section introduction
```text
   6.23   WAVeform     Group

 The commands in this group deal with the output of the retrieved waveform display data.
 There are no front panel keys that correspond to the commands in this group.
```
### Left column
```text
 :WAVeform?
 Function Queries all settings related to the output of
       waveform display data.
 Syntax :WAVeform?
 Example :WAVEFORM? -> :WAVEFORM:TRACE U1;
       FORMAT ASCII;START 0;END 1001;
       HOLD 0

 :WAVeform:BYTeorder
 Function Sets the output byte order of the waveform
       display data (FLOAT format) that is transmitted
       by “:WAVeform:SEND?” or queries the current
       setting.
 Syntax :WAVeform:BYTeorder {LSBFirst|
       MSBFirst}
       :WAVeform:BYTeorder?
 Example :WAVEFORM:BYTEORDER LSBFIRST
       :WAVEFORM:BYTEORDER? ->
       :WAVEFORM:BYTEORDER LSBFIRST
 Description This value is valid when “:WAVeform:FORMat”
       is set to “{FLOat}.”
 :WAVeform:END
 Function Sets the output end point of the waveform display
       data that is transmitted by “:WAVeform:SEND?”
       or queries the current setting.
 Syntax :WAVeform:END {<NRf>}
       :WAVeform:END?
       <NRf> = 0 to 1001
 Example :WAVEFORM:END 1001
       :WAVEFORM:END? ->
       :WAVEFORM:END 1001
 :WAVeform:FORMat
 Function Sets the format of the waveform display data that
       is transmitted by “:WAVeform:SEND?” or queries
       the current setting.
 Syntax :WAVeform:FORMat {ASCii|FLOat}
       :WAVeform:FORMat?
 Example :WAVEFORM:FORMAT FLOAT
       :WAVEFORM:FORMAT? -> :WAVEFORM:FORMAT
       FLOAT
 Description For the differences in the waveform display
       data output due to the format setting, see the
       description for “:WAVeform:SEND?.”
```
### Right column
```text
 :WAVeform:HOLD
 Function Sets whether to hold (ON) or release (OFF) all
       the waveform display data or queries the current
       setting.
 Syntax :WAVeform:HOLD {<Boolean>}
       :WAVeform:HOLD?
 Example :WAVEFORM:HOLD ON
       :WAVEFORM:HOLD? -> :WAVEFORM:HOLD 1
 Description • If :WAVeform:HOLD is turned ON before
        executing “:WAVeform:SEND?,” all the
        waveform data at that point can be held
        internally.
       • As long as :WAVeform:HOLD is ON, the
        waveform data is held even when the
        waveform display on the screen is updated.
       • For example, if you wish to retrieve the
        waveform display data of U1 and I1 at the
        same point, do the following:
        :WAVeform:HOLD ON
        :WAVeform:TRACe U1
        :WAVeform:SEND?
        (Receive the waveform display data of U1)
        :WAVeform:TRACe I1
        :WAVeform:SEND?
        (Receive the waveform display data of I1)
       :WAVeform:HOLD OFF
       • If ON is specified when :WAVeform:HOLD
        is ON, the waveform display data is cleared
        once, and the most recent waveform data is
        held internally. This method can be used when
        retrieving waveform display data continuously
        (no need to set :WAVeform:HOLD to OFF
        each time).
 :WAVeform:LENGth?
 Function Queries the total number of points of the
       waveform specified by :WAVeform:TRACe.
 Syntax :WAVeform:LENGth?
 Example :WAVEFORM:LENGTH? -> 1002
 Description The number of data points is fixed. “1002” is
       always returned.
```

## Page 6-113

### Left column
```text
   :WAVeform:SEND?
   Function Queries the waveform display data specified by
         “:WAVeform:TRACe”.
   Syntax :WAVeform:SEND?
   Example • When “:WAVeform:FORMat” is set to
          {ASCii}
          :WAVEFORM:SEND? -> <NR3>,<NR3>,...
         • When “:WAVeform:FORMat” is set to
          {FLOat}
          :WAVEFORM:SEND? -> #4(number of bytes, 4
          digits)(data byte sequence)
   Description • The format of the waveform display data
          that is output varies depending on the
          “:WAVeform:FORMat” setting as follows:
           (1) When “ASCii” is specified
             The physical value is output in the <NR3>
             format. The data of each point is delimited
             by a comma.
           (2) When “FLOat” is specified
             The physical value is output in IEEE
             single-precision floating point (4-byte)
             format.
             The output byte order of the data of each
             point follows the order that is set using the
             “:WAVeform:BYTeorder” command.
         • If there is no waveform display data even when
          the display mode (:DISPlay:MODE) is set to a
          mode to display waveforms, the data is output
          as follows:
           (1) When “ASCii” is specified
             The data of all points are output as “NAN.”
           (2) When “FLOat” is specified
             The data of all points are output as
             “0(0x00000000).”
   :WAVeform:SRATe?
   Function Queries the sample rate of the retrieved
         waveform.
   Syntax :WAVeform:SRATe?
   Example :WAVEFORM:SRATE? -> 200.000E+03
   :WAVeform:STARt
   Function Sets the output start point of the waveform display
         data that is transmitted by “:WAVeform:SEND?”
         or queries the current setting.
   Syntax :WAVeform:STARt {<NRf>}
         :WAVeform:STARt?
         <NRf> = 0 to 1001
   Example :WAVEFORM:START 0
         :WAVEFORM:START? ->
         :WAVEFORM:START 0
```
### Right column
```text
                  6.23 WAVeform Group

 :WAVeform:TRACe
 Function Sets the target waveform for “:WAVeform:SEND?”
       or queries the current setting.
 Syntax :WAVeform:TRACe {U<x>|I<x>|SPEed|
       TORQue|MATH<x>}
       :WAVeform:TRACe?
       <x> of U<x>, I<x> = 1 to 4 (element)
       <x> of MATH<x> = 1 to 2 (MATH)
 Example :WAVEFORM:TRACE U1
       :WAVEFORM:TRACE? ->
       :WAVEFORM:TRACE U1
 Description {SPEed|TORQue} are valid only on models with
       the motor evaluation function (/MTR option).
 :WAVeform:TRIGger?
 Function Queries the trigger position of the retrieved
       waveform.
 Syntax :WAVeform:TRIGger?
 Example :WAVEFORM:TRIGGER? -> 0
 Description Since the trigger position is always at the
       beginning of the waveform display data, “0” is
       returned.
```

## Page 6-114

### Section introduction
```text
   6.24   Common      Command     Group

 The commands in the common group are defined in the IEEE488.2-1992 and are independent of the instrument’s
 functions. There are no front panel keys that correspond to the commands in this group.
```
### Left column
```text
 *CAL?(CALibrate)
 Function Executes zero calibration (zero-level
       compensation, same operation as pressing CAL
       (SHIFT+SINGLE)) and queries the result.
 Syntax *CAL?
 Example *CAL? -> 0
 Description If the calibration terminates normally, 0 is
       returned. If an error is detected, 1 is returned.

 *CLS(CLear Status)
 Function Clears the standard event register, extended
       event register, and error queue.
 Syntax *CLS
 Example *CLS
 Description • If the *CLS command is located immediately
        after the program message terminator, the
        output queue is also cleared.
       • For details on the register and queue, see
        chapter 7.
 *ESE
 (standard Event Status Enable
 register)
 Function Sets the standard event enable register or
       queries the current setting.
 Syntax *ESE {<NRf>}
       *ESE?
       <NRf> = 0 to 255
 Example *ESE 251
       *ESE? -> 251
 Description • Specify the value as a sum of decimal values
        of each bit.
       • For example, specifying “*ESE 251” will cause
        the standard enable register to be set to
        “11111011.” In this case, bit 2 of the standard
        event register is disabled which means that bit
        5 (ESB) of the status byte register is not set to 1,
        even if a “query error” occurs.
       • The default value is “*ESE 0” (all bits
        disabled).
       • A query using *ESE? will not clear the contents
        of the standard event enable register.
       • For details on the standard event enable
        register, see page 7-5.
```
### Right column
```text
 *ESR?(standard Event Status Register)
 Function Queries the standard event register and clears
       the register.
 Syntax *ESR?
 Example *ESR? -> 32
 Description • A sum of decimal values of each bit is returned.
       • You can check what type of events occurred
        when an SRQ is generated.
       • For example, if a value of “32” is returned, this
        indicates that the standard event register is set
        to “00100000.” In this case, you can see that
        the SRQ occurred due to a “command syntax
        error.”
       • A query using *ESR? will clear the contents of
        the standard event register.
       • For details on the standard event register, see
        page 7-5.
 *IDN?(IDeNtify)
 Function Queries the instrument model.
 Syntax *IDN?
 Example *IDN? ->
       YOKOGAWA,WT3004E-2A0-30A4,0,F6.01
 Description • The information is returned in the following
        form: <Manufacturer>,<Model>,<Serial
        No.>,<Firmware version>
       • <Model> is in the format “model (7 digits)-2 A
        input element configuration (3 digits)-30 A input
        element configuration (4 digits)” For details on
        the model code and input element structure,
        see “Checking the Contents of the Package” in
        the user’s manual, IM WT3001E-01EN.
       • In actuality, <Serial No.> is not returned
        (always 0).
```

## Page 6-115

### Left column
```text
   *OPC(OPeration Complete)
   Function Sets bit 0 (OPC bit) of the standard event register
         to 1 upon the completion of the specified overlap
         command.
   Syntax *OPC
   Example *OPC
   Description • For the description regarding how to
          synchronize the program using *OPC, see
          page 5-9.
         • The “COMMunicate:OPSE” command is used
          to specify the overlap command.
         • If *OPC is not the last command of the
          message, the operation is not guaranteed.
   *OPC?(OPeration Complete)
   Function ASCII code “1” is returned when the specified
         overlap command is completed.
   Syntax *OPC?
   Example *OPC? -> 1
   Description • For the description regarding how to
          synchronize the program using *OPC?, see
          page 5-9.
         • The “COMMunicate:OPSE” command is used
          to specify the overlap command.
         • If *OPC? is not the last command of the
          message, the operation is not guaranteed.
   *OPT?(OPTion)
   Function Queries the installed options.
   Syntax *OPT?
   Example *OPT? ->G6,B5,FQ,DA,V1,C2,C7,C5,FL,
         MTR
   Description • The presence or absence of the following is
          returned: harmonic computation function (G6),
          built-in printer (B5), frequency measurement
          addition (FQ), 20chDA output (DA), VGA output
          (V1), RS-232 communications (C2), USB port
          (for PC, C12), Ethernet (C7), USB port (for
          peripherals, C5), measurement (FL), and motor
          evaluation function (MTR).
         • If none of the options is installed, an ASCII
          code “0” is returned.
         • The *OPT? query must be the last query of the
          program message. An error occurs if there is a
          query after this query.
```
### Right column
```text
             6.24 Common Command Group

 *PSC(Power-on Status Clear)
 Function Sets whether to clear the registers below at
       power on or queries the current setting. The
       register is cleared when the value rounded to an
       integer is a non-zero value.
       • Standard event enable register
       • Extended event enable register
       • Transition filter
 Syntax *PSC {<NRf>}
       *PSC?
       <NRf> = 0 (not clear), non-zero (clear)
 Example *PSC 1
       *PSC? -> 1
 Description For details on the registers, see chapter 7.
 *RST(ReSeT)
 Function Initializes the settings.
 Syntax *RST
 Example *RST
 Description • Also clears *OPC and *OPC? commands that
        have been sent earlier.
       • All settings except communication settings are
        reset to factory default values.
 *SRE(Service Request Enable register)
 Function Sets the service request enable register or
       queries the current setting.
 Syntax *SRE {<NRf>}
       *SRE?
       <NRf> = 0 to 255
 Example *SRE 239
       *SRE? -> 175(since the bit 6 (MSS) setting is
       ignored)
 Description • Specify the value as a sum of decimal values
        of each bit.
       • For example, specifying “*SRE 239” will
        cause the service request enable register to
        be set to “11101111.” In this case, bit 4 of the
        service request enable register is disabled
        which means that bit 4 (MAV) of the status
        byte register is not set to 1, even if “the output
        queue is not empty.”
       • Bit 6 (MSS) of the status byte register is the
        MSS bit itself, and therefore, is ignored.
       • The default value is “*SRE 0” (all bits disabled).
       • A query using *SRE? will not clear the contents
        of the service request enable register.
       • For details on the service request enable
        register, see page 7-3.
```

## Page 6-116

### Left column
```text
 6.24 Common Command Group

 *STB?(STatus Byte)
 Function Queries the status byte register.
 Syntax *STB?
 Example *STB? -> 4
 Description • The sum of the bits is returned as a decimal
        value.
       • Since the register is read without executing
        serial polling, bit 6 is a MSS bit not RQS.
       • For example, if a value of 4 is returned, this
        indicates that the status byte register is set to
        “00000100.” In this case, you can see that “the
        error queue is not empty” (an error occurred).
       • A query using *STB? will not clear the contents
        of the status byte register.
       • For details on the status byte register, see
        page 7-3.
 *TRG(TRiGger)
 Function Executes single measurement (the same
       operation as when SINGLE is pressed).
 Syntax *TRG
 Example *TRG
 Description The multi-line message GET (Group Execute
       Trigger) also performs the same operation as this
       command.
 *TST?(TeST)
 Function Performs a self-test and queries the result.
 Syntax *TST?
 Example *TST? -> 0
 Description • The self-test involves internal memory tests.
       • “0” is returned if the self-test is successful, “1”
        if it is not.
       • It takes approximately 90 s for the test to
        complete. When receiving a response from this
        instrument, set the timeout to a relatively large
        value.
 *WAI(WAIt)
 Function Holds the subsequent command until the
       completion of the specified overlap operation.
 Syntax *WAI
 Example *WAI
 Description • For the description regarding how to
        synchronize the program using *WAI, see page
        5-8.
       • The “COMMunicate:OPSE” command is used
        to specify the overlap command.
```
