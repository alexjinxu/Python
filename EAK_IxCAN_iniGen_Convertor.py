import os
class EAK_ICan_Map:
    def __init__(self):

        self.PointNameOutput=["DP01","DP02","DP03","DP04","DP05","DP06","DP07","DP08","DP09","DP10","DP11","DP12","DP13",
                              "DP14","DP15","DP16","DP17","DP18","DP19","DP20","DP21","DP22","DP23","DP24","DP25",
                              "DP26","DP27","DP28","DP29","DP30","DP31","DP32"]

        self.PointAddressOutput=["0x7F01","0x7F02","0x7F03","0x7F04","0x7F05","0x7F06","0x7F07","0x7F08","0x7F09","0x7F10",
                                 "0x7F11","0x7F12","0x7F13","0x7F14","0x7F15","0x7F16","0x7F17","0x7F18","0x7F19","0x7F20",
                                 "0x7F21","0x7F22","0x7F23","0x7F24","0x7F25","0x7F26","0x7F27","0x7F28","0x7F29","0x7F30",
                                 "0x7F31","0x7F32"]


        self.TargetPosition=False

        self.IxCan_COM_dict={1:0,43:1,2:2,44:3,3:4,45:5,4:6,46:7,5:8,47:9,6:10,48:11,7:12,49:13,
                       8:14,50:15,9:16,51:17,10:18,52:19,11:20,53:21,12:22,54:23,13:24,55:25,
                       14:26,56:27,15:28,57:29,16:30,58:31}



    def open_Wayside_DB_projData(self, filename):
        originalDataInputSuccessful =False
        lines=open(filename)

        for line in lines:

            line.strip()

            line=line.replace("\n","")

            if ("Zp"==line and self.TargetPosition == False):

                self.TargetPosition = True
                continue

            #assert (self.TargetPosition == True and len(line)==0), "original data input fail" # need investigation of assert statement

            if (len(line) == 0 and originalDataInputSuccessful == True and self.TargetPosition == True ):
                self.TargetPosition =False
                print("OriginalDataMappedSuccessfully")
                break

            if ( (self.TargetPosition == True) and (len(line)!=0)):
                originalDataInputSuccessful = True

                temp_line = line

                Ix, Name, ZpAdr, IxCAN, ZpTO = temp_line.split(",",4)

                IxCAN=eval(IxCAN)
                ZpAdr=eval(ZpAdr)
                Name=eval(Name)

                temp_Garbage, IxCANdictIndx = IxCAN.split('=',1)

                IxCANdictIndx=int(IxCANdictIndx)

              #  assert (IxCANdictIndx >=0 and IxCANdictIndx <=31 ), "IxCAN value over the range (1,32)"

                temp_Garbage, ZpAdrvalue = ZpAdr.split('=', 1)

                temp_Garbage, Namevalue = Name.split('=', 1)

                try:
                    outputIdx =self.IxCan_COM_dict[IxCANdictIndx]
                    assert (outputIdx >= 0 and outputIdx <= 31), "index value over the range (0,31)"
                    self.PointNameOutput[outputIdx]= Namevalue
                    self.PointAddressOutput[outputIdx] = ZpAdrvalue
                except KeyError:
                    print("IxCANdictIndx does not find in dict")
        lines.close()


    def write_Output_file(self, filename):
        outputfile =open(filename,'w')
        # ouput file header print

        print("[ALLGEMEIN]",file=outputfile)
        print("",file=outputfile)
        print("// Telegram cycle in milliseconds", file=outputfile)
        print("Cycle=200", file=outputfile)
        print("",file=outputfile)
        print("// Serial interface settings", file=outputfile)
        print("Baudrate=9600", file=outputfile)
        print("Bits=8", file=outputfile)
        print("Parity=E", file=outputfile)
        print("StopBits=1", file=outputfile)
        print("", file=outputfile)
        print("// COM-Port of each serial interface", file=outputfile)
        for i  in range(1,33):
            print("Port",i,"=//./COM",i+9,sep='',file=outputfile)
        print("", file=outputfile)
        print("", file=outputfile)


        # print Point Name
        print("// Name of each Detection Point", file=outputfile)
        for i in range (0,32):
            print("Name", i+1, "=", self.PointNameOutput[i], sep='', file=outputfile)
        print("\n", file=outputfile)

        # print Point Name
        print("// Address of each Detection Point", file=outputfile)
        for i in range(0, 32):
            print("Address", i + 1, "=", self.PointAddressOutput[i], sep='', file=outputfile)

        outputfile.close()

if __name__ == '__main__':

    version = input("Please Input Versoin Number:")

    outputfoldername = "EAK_sim"
    outputfolder = os.path.exists(outputfoldername)


    if not outputfolder:

        os.makedirs(outputfoldername)


    logfilename = "EAK_IxCNA_iniGen.log"
    logfilepathname=os.path.join(outputfoldername,logfilename)
    #logfile = open("EAK_IxCNA_iniGen.log", 'w')
    logfile = open(logfilepathname, 'w')
    for root, dirs, files in os.walk(".", topdown=True):
        for name in files:
            if (os.path.splitext(name)[1] == '.dat'):
                InputFileName = os.path.join(root,name)
                Preflex, tail = name.split("_", 1)
                OutputFileName = Preflex.upper() + "_" + version+ ".ini"
                outputfilenamepath =os.path.join(outputfoldername,OutputFileName)
                print("Input Data File Name  ->", InputFileName,file=logfile)
                print("Gener ini  File Name  ->", outputfilenamepath, file=logfile)
                EAK_Gen = EAK_ICan_Map()
                EAK_Gen.open_Wayside_DB_projData(InputFileName)
                EAK_Gen.write_Output_file(outputfilenamepath)
    input('press enter any key to exit')
    