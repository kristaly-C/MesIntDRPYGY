import tkinter
import tkinter.messagebox
from tkinter.ttk import Label
import customtkinter
import grafdraw
import VRPPD

customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("green")  # Themes: "blue" (standard), "green", "dark-blue"


class App(customtkinter.CTk):
    maxcity = 100
    cityNum = 5
    tabuNum = 0
    courierNum = 1
    pairNum = 0
    seed = 0
    cycle = 100
    def __init__(self):
        super().__init__()


        self.title("VRPPD problem solver")
        self.geometry(f"{400}x{580}")
        self.minsize(400,500)
        
        # create grid 
        self.grid_rowconfigure((0,1,2,3,4,5,6), weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        #slider varosok
        self.varos_frame = customtkinter.CTkFrame(self,)
        self.varos_frame.grid(row = 0, column=0, sticky="nsew")
        self.varos_frame.grid_rowconfigure( (0, 1,2), weight=1)
        self.varos_frame.grid_columnconfigure(0, weight=1)
        self.lab1 = customtkinter.CTkLabel(self.varos_frame, text="Number of cities:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.lab1.grid(row=0, column=0, padx=10, sticky="ew")
        self.slider_varos = customtkinter.CTkSlider(self.varos_frame, from_=5, to= self.maxcity, number_of_steps= self.maxcity-5, variable=tkinter.IntVar(value=5) , command=self.setCityVar)
        self.slider_varos.grid(row=1, column=0, padx=(20, 10), sticky="ew")
        self.labnum1 = customtkinter.CTkLabel(self.varos_frame, text= self.cityNum, font=customtkinter.CTkFont(size=15))
        self.labnum1.grid(row=2, column=0, padx=10, sticky="ew")
        
        #slider futarok
        self.futar_frame = customtkinter.CTkFrame(self,)
        self.futar_frame.grid(row = 1, column=0, sticky="nsew")
        self.futar_frame.grid_rowconfigure( (0, 1,2), weight=1)
        self.futar_frame.grid_columnconfigure(0, weight=1)
        self.lab1 = customtkinter.CTkLabel(self.futar_frame, text="Number of courier:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.lab1.grid(row=0, column=0, padx=10, sticky="ew")
        self.slider_futar = customtkinter.CTkSlider(self.futar_frame, from_=1, to=2, number_of_steps=1, variable=tkinter.IntVar(value=0),state = tkinter.DISABLED , command=self.setCourier)
        self.slider_futar.grid(row=1, column=0, padx=(20, 10), sticky="ew")
        self.labnum3 = customtkinter.CTkLabel(self.futar_frame, text= 0, font=customtkinter.CTkFont(size=15))
        self.labnum3.grid(row=2, column=0, padx=10, sticky="ew")
        
        #slider tabusize
        self.varos_frame = customtkinter.CTkFrame(self,)
        self.varos_frame.grid(row = 2, column=0, sticky="nsew")
        self.varos_frame.grid_rowconfigure( (0, 1,2), weight=1)
        self.varos_frame.grid_columnconfigure(0, weight=1)
        self.lab1 = customtkinter.CTkLabel(self.varos_frame, text="Tabu array size:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.lab1.grid(row=0, column=0, padx=10, sticky="ew")
        self.slider_tabu = customtkinter.CTkSlider(self.varos_frame, from_=0, to=100, number_of_steps=100, variable=tkinter.IntVar(value=0) , command=self.setTabu)
        self.slider_tabu.grid(row=1, column=0, padx=(20, 10), sticky="ew")
        self.labnum4 = customtkinter.CTkLabel(self.varos_frame, text= 0, font=customtkinter.CTkFont(size=15))
        self.labnum4.grid(row=2, column=0, padx=10, sticky="ew")
        
        #slider parok
        self.pair_frame = customtkinter.CTkFrame(self,)
        self.pair_frame.grid(row = 3, column=0, sticky="nsew")
        self.pair_frame.grid_rowconfigure( (0, 1,2), weight=1)
        self.pair_frame.grid_columnconfigure(0, weight=1)
        self.lab1 = customtkinter.CTkLabel(self.pair_frame, text="Number of couples:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.lab1.grid(row=0, column=0, padx=10, sticky="ew")
        self.slider_par = customtkinter.CTkSlider(self.pair_frame, from_=0, to=1, number_of_steps=1, variable=tkinter.IntVar(value=0) , command=self.setCityPair)
        self.slider_par.grid(row=1, column=0, padx=(20, 10), sticky="ew")
        self.labnum2 = customtkinter.CTkLabel(self.pair_frame, text= 0, font=customtkinter.CTkFont(size=15))
        self.labnum2.grid(row=2, column=0, padx=10, sticky="ew")
        
        #randomseed
        self.entry = customtkinter.CTkEntry(self, textvariable= tkinter.StringVar(value=5))
        self.entry.grid(row=4, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")

        #slider cycle
        self.cycle_frame = customtkinter.CTkFrame(self,)
        self.cycle_frame.grid(row = 5, column=0, sticky="nsew")
        self.cycle_frame.grid_rowconfigure( (0, 1,2), weight=1)
        self.cycle_frame.grid_columnconfigure(0, weight=1)
        self.lab5 = customtkinter.CTkLabel(self.cycle_frame, text="Number of cycle:", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.lab5.grid(row=0, column=0, padx=10, sticky="ew")
        self.slider_cycle = customtkinter.CTkSlider(self.cycle_frame, from_=100, to=10000, number_of_steps=99, variable= tkinter.IntVar(value=100) , command=self.setCycle)
        self.slider_cycle.grid(row=1, column=0, padx=(20, 10), sticky="ew")
        self.labnum5 = customtkinter.CTkLabel(self.cycle_frame, text= int(self.slider_cycle.get()), font=customtkinter.CTkFont(size=15))
        self.labnum5.grid(row=2, column=0, padx=10, sticky="ew")
        
        #gomb futtatas
        self.button = customtkinter.CTkButton(master=self, command=self.submit,state = tkinter.DISABLED, text="Run")
        self.button.grid(row=6, column=0, padx=20, pady=20, sticky="ew")

    def setCityVar(self, output):
        self.labnum1.configure(text= int(output))
        self.cityNum = int(output)

        if (output//2)-1 <=0:
            minPairSet = 1
        else:
             minPairSet = (output//2)-1
        self.slider_par.configure(to=minPairSet, variable=tkinter.IntVar(value=int(self.slider_par.get())), number_of_steps= minPairSet)
        self.pairNum = int(self.slider_par.get())
        self.labnum2.configure(text= int(self.slider_par.get()))
        self.courierControl(output)
        
        self.checkValidity()

    def setCityPair(self, output):
        self.labnum2.configure(text= int(output))
        self.pairNum = int(output)

    def setCourier(self, output):
        self.labnum3.configure(text= int(output))
        self.courierNum = int(output)

    def setTabu(self, output):
        self.labnum4.configure(text= int(output))
        self.tabuNum = int(output)

    def setCycle(self, output):
        self.labnum5.configure(text= int(output))
        self.cycle = int(output)

    def courierControl(self,citynum):
        if citynum > 9:
            maxFutar = int(citynum/5)
            self.slider_futar.configure(state = tkinter.NORMAL)
            if maxFutar > 20 :
                maxFutar = 20
            slFut = int(self.slider_futar.get())
            self.slider_futar.configure(to= maxFutar, variable= tkinter.IntVar(value=slFut), number_of_steps= int(maxFutar-1))
            self.courierNum = slFut
            self.labnum3.configure(text= slFut)
        else:
            self.courierNum = 1
            self.slider_futar.configure(state = tkinter.DISABLED)
            self.slider_futar.set(1)
            self.labnum3.configure(text= int(self.slider_futar.get()))
        
        

    def checkValidity(self):
        valid = [0,0]
        if self.cityNum > 4 and self.cityNum < self.maxcity :
            valid[0] = 1
        else:
            valid[0] = 0

        if self.pairNum < self.cityNum/2 and self.pairNum >= 0:
            valid[1] = 1
        else:
            valid[1] = 0

        
        if sum(valid) == 2:
            self.button.configure(state = tkinter.NORMAL)
        else:
            self.button.configure(state = tkinter.DISABLED)

    def submit(self):
        try:
            seed = int(self.entry.get())
        except ValueError:
            seed = 5
        print(self.tabuNum, self.courierNum, self.cityNum, self.pairNum, seed, self.cycle)
        generatedCities = VRPPD.datagen(self.cityNum,seed,0,300)
        fullLenght, BestRoutes, BestroutsLengts = VRPPD.VRPPDCalc(generatedCities,self.courierNum,self.tabuNum,self.pairNum,self.cycle,(10,10))
        self.openNewWindow(BestRoutes,BestroutsLengts,fullLenght,generatedCities)
    
    def testFg(self, generatedCities,BestRoutes):
        grafdraw.graphDraw(generatedCities,BestRoutes,(10,10))

    def openNewWindow(self,routeLists,RouteLengts,fullLenght,generatedCities):
        #window setup
        window = customtkinter.CTkToplevel(self)
        window.geometry("600x400")
        x = self.winfo_x()
        y = self.winfo_y()
        window.geometry("+%d+%d" %(x+400,y))
        window.grid_rowconfigure(0, weight=3)
        window.grid_rowconfigure(1, weight=1)
        window.grid_columnconfigure(0, weight=1)
        #databox
        resultTexBox = customtkinter.CTkTextbox(window)
        resultTexBox.grid(row=0, column=0, padx=10, pady=10, sticky='news')
        #process data
        text = str()
        for i in range(len(routeLists)):
            inf = str(i)  + ". route lenght: " + str(RouteLengts[i]) + "\n S->"
            text = text + inf
            ruu = str()
            for j in range(len(routeLists[i])):
                conc = str(routeLists[i][j]) + "->"
                ruu = str(ruu + conc)
            text = text + ruu + "S \n"
        text = text + "Length of the total space covered: " + str(fullLenght)
        resultTexBox.insert("end", text)
        resultTexBox.configure(state="disabled")
        #button
        exportButton = customtkinter.CTkButton(window,text="Graph", command= lambda : self.testFg(generatedCities,routeLists))
        exportButton.grid(row=1, column=0, padx=10, pady=10, sticky="ew")
        if self.courierNum > 10:
            exportButton.configure(state= tkinter.DISABLED)



if __name__ == "__main__":
    app = App()
    app.mainloop()