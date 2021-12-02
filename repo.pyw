import datetime
from tkinter import *

try:
    from PIL import ImageTk, Image
except:
    import os
    os.system("pip install pillow")
    from PIL import ImageTk, Image

from functions import *
from tkinter.filedialog import askopenfilenames

root = Tk()
root.title("REPO")
root.iconbitmap("resources/repo.ico")

#GLOBAL VARIABLES
userName = "Admin"
userId = 1

#IMAGES
logoImage = ImageTk.PhotoImage(Image.open("resources/repo_pequeno.png"))
profileImage = ImageTk.PhotoImage(Image.open("resources/usuario2.png").resize((26,26)))
configImage = ImageTk.PhotoImage(Image.open("resources/configuraciones.png").resize((22,22)))
searchImage = ImageTk.PhotoImage(Image.open("resources/lupa.png").resize((18,18)))
editImage = ImageTk.PhotoImage(Image.open("resources/editar-texto.png").resize((24,24)))
eventImages = []
auxImg = []
viewImg = 0

#LOG IN SCREEN
def loginScreen():
    for child in root.winfo_children():
        child.destroy()
    def logInButtonCommand():
        name = userNameEntry.get()
        password = userPasswordEntry.get()

        if(validLogin(name, password) == -1):
            failLoginLabel.config(fg="#FF0000")
        else:
            global userName
            global userId
            userName = name
            userId = validLogin(name, password)
            mainScreen()

    canvas = Canvas(root, width=750, height=500, bg="#6EDA6C")
    canvas.grid(column=0, row=0, columnspan=4, rowspan=21)

    logoImageLabel = Label(root, image= logoImage, background="#6EDA6C")
    logoImageLabel.grid(column=1, row=6, columnspan=2)

    logInLabel = Label(root, text="Inicio de Sesion", font=("Calibri", 29, "bold"), background="#6EDA6C")
    logInLabel.grid(column=1, row=7, columnspan=2)

    userNameLabel = Label(root, text="Nombre de usuario", font= ("calibri", 19), background="#6EDA6C")
    userNameLabel.grid(column=1, row=8, columnspan=2)
    userNameEntry = Entry(root, font=("calibri", 19))
    userNameEntry.grid(column=1, row=9, columnspan=2)
    userNameEntry.focus()

    userPasswordLabel = Label(root, text="Contraseña", font= ("calibri", 19), background="#6EDA6C")
    userPasswordLabel.grid(column=1, row=10, columnspan=2)
    userPasswordEntry = Entry(root, font=("calibri", 19), show="*")
    userPasswordEntry.grid(column=1, row=11, columnspan=2)

    failLoginLabel = Label(root, text="La contraseña y/o usuario son incorrectos", bg="#6EDA6C", fg="#6EDA6C", font = ("arial", 13))
    failLoginLabel.grid(column=1, row=13, columnspan=2)

    logInButton = Button(root, text="Entrar", font=("Calibri", 15), pady=0, background="#3BB538", command=logInButtonCommand, relief="flat", padx=20, foreground="#FFFFFF")
    logInButton.grid(column=1, row=15, columnspan=2)

#MAIN REPO SCREEN
def mainScreen():
    global logoImage
    global eventImages
    eventImages = []

    for child in root.winfo_children():
        child.destroy()

    canvas = Canvas(root, width=750, height=500, bg="#D1FFD0")
    canvas.grid(column=0, row=0, columnspan=5, rowspan=75)
    
    #PROFILE BOX:
    #Frame:
    profileFrame = Frame(root, background="#D1FFD0", name="profile name", border=0, relief="solid")
    profileFrame.grid(column=0, row=0, sticky=W, padx=20, pady=0)
    #image
    profileImageLabel = Label(profileFrame, image= profileImage, background="#D1FFD0", border=0, relief="solid")
    profileImageLabel.grid(column=0, row=0)
    #User Name
    profileNameLabel = Label(profileFrame, text=userName, background="#D1FFD0", font=("calibri", 16), border=0, relief="solid")
    profileNameLabel.grid(column=1, row=0, padx=10)
    #Configs Button
    configsButton = Button(profileFrame, image= configImage, background="#6EDA6C", fg="#D1FFD0", command=configScreen)
    configsButton.grid(column=2, row=0)

    #create event button
    createEventButton = Button(root, text= "Crear Evento +", font=("calibri", 16, "bold"), bg="#6EDA6C", relief="flat", pady=0, command=createEventScreen)
    createEventButton.grid(column=4, row=0, sticky=E, padx=10, pady=5)

    #logo
    logoImage = ImageTk.PhotoImage(Image.open("resources/repo_pequeno.png").resize((117, 41)))
    logoImageLabel = Label(root, image= logoImage, background="#D1FFD0", border=0, relief="solid")
    logoImageLabel.grid(column=0, row=1, columnspan=5, pady=0)

    #Search event button
    searchEventButton = Button(root, image=searchImage, text="Buscar", compound="left", padx=10, font=("Calibri", 13), background="#6EDA6C", command=filterEventsScreen)
    searchEventButton.grid(column=4, row=2, sticky="e", padx=20)

    #EVENTS FRAME & TITLE
    eventsTitleLabel = Label(root, text="Eventos", font=("calibri", 19), background="#D1FFD0", border=0, relief="solid")
    eventsTitleLabel.grid(column=0, row=2, sticky="w", padx=20)

    eventsFrame = Frame(root)
    eventsFrame.grid(row=3, column=0, columnspan=5, rowspan=72)

    eventsCanvas = Canvas(eventsFrame, height=320, width=710)
    eventsCanvas.grid(row=0, column=0)
    scrollbar = Scrollbar(eventsFrame, orient="vertical", command=eventsCanvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    eventsCanvas.configure(yscrollcommand=scrollbar.set)
    eventsCanvas.bind("<Configure>", lambda e: eventsCanvas.configure(scrollregion=eventsCanvas.bbox("all")))

    eventsContainer = Frame(eventsCanvas, background="#D1FFD0")
    eventsContainer.grid(column=0, row=3, columnspan=5, rowspan=72)
    auxCanvas = Canvas(eventsContainer, width= 710, height=320, background="#B4FFB2", relief="flat")

    eventsCanvas.create_window((0,0), window=eventsContainer, anchor="n")

    events = getAllEvents()
    auxCanvas.grid(column=0, row=0, columnspan=4, rowspan=len(events)//4 + 1 if (len(events)//4 + 1 >= 4) else 4, sticky="ns")

    eventIndex = 0
    for row in range(len(events)//4 + 1):
        for column in range(4):
            try:
                events[eventIndex]
            except:
                pass
            else:
                binImage = getImages(events[eventIndex][0])
                if(len(binImage) > 0):
                    open("resources/auxImg.jpg", "wb").write(binImage[0][0])
                    eventImages += [ImageTk.PhotoImage(Image.open("resources/auxImg.jpg").resize((160,90)))]
                else:
                    eventImages += [ImageTk.PhotoImage(Image.open("resources/noimgyet.jpg"))]
                
                Button(eventsContainer, relief="flat", text=events[eventIndex][1], image=eventImages[eventIndex], compound="top", command=lambda x = events[eventIndex][0]: eventScreen(x)).grid(row=row, column=column, padx=0, pady=15, sticky=N)
            eventIndex += 1

#SCREEN TO CREATE A NEW EVENT
def createEventScreen():
    #clearing the main window
    for child in root.winfo_children():
        child.destroy()
    #Setting background
    canvas = Canvas(root, width=750, height=500, bg="#D1FFD0")
    canvas.grid(column=0, row=0, columnspan=5, rowspan=75)

    #Function to add a new event to the database
    def createButtonFunction():
        # Preparing the data to pass to the "AddEvent Func"
        name = eventNameEntry.get()
        date = f"{yearEntry.get()}-{monthEntry.get()}-{dayEntry.get()}"
        location = locationEntry.get()
        if not(name and date and location):
            warningLabel.configure(fg="red", text="Todos los campos deben estar llenos")
        elif(len(yearEntry.get()) + len(monthEntry.get()) + len(dayEntry.get()) < 8):
            warningLabel.configure(fg="red", text="La fecha debe estar completa (DD, MM, YYYY)")
        else:
            eventID = addEvent(name, date, location, userId)
            eventScreen(eventID)

    #profile box
    profileFrame = Frame(root, background="#D1FFD0", name="profile name", border=1, relief="flat")
    profileFrame.grid(column=0, row=0, sticky=W, padx=10, pady=5)
    profileImageLabel = Label(profileFrame, image= profileImage, background="#D1FFD0")
    profileImageLabel.grid(column=0, row=0)
    profileNameLabel = Label(profileFrame, text=userName, background="#D1FFD0", font=("calibri", 16))
    profileNameLabel.grid(column=1, row=0, padx=10)

    #Title Label
    titleLabel = Label(root, text="Creando Evento", font=("calibri", 30), background="#D1FFD0")
    titleLabel.grid(columnspan=5, row=1, column=0, pady=20)

    #Entrys:
    #Event Name
    eventNameLabel = Label(root, text="Nombre del evento", font=("Calibri", 22), background="#D1FFD0")
    eventNameLabel.grid(columnspan=5, row=2, column=0)
    eventNameEntry = Entry(root, font=("Calibri", 19), width=20, relief="solid", border=1)
    eventNameEntry.grid(columnspan=5, row=3, column=0)
    eventNameEntry.focus()
    #location
    locationLabel = Label(root, text="Ubicacion", font=("Calibri", 22), background="#D1FFD0")
    locationLabel.grid(columnspan=5, row=6, column=0)
    locationEntry = Entry(root, font=("Calibri", 19), width=20, relief="solid", border=1)
    locationEntry.grid(columnspan=5, row=7, column=0)
    #DATE
    #Date title
    dateLabel = Label(root, text="Fecha", font=("Calibri", 22), background="#D1FFD0")
    dateLabel.grid(columnspan=5, row=4, column=0)
    #frame to contain the entrys
    dateFrame = Frame(root, bg="#D1FFD0")
    dateFrame.grid(columnspan=5, row=5, column=0)
    #year label and entry
    yearLabel = Label(dateFrame, text="Año: ", font=("Calibri", 19), background="#D1FFD0")
    yearLabel.grid(column=4, row=0)
    yearEntry = Entry(dateFrame, font=("Calibri", 16), width=4, relief="solid", border=1)
    yearEntry.grid(column=5, row=0)
    #month label and entry
    monthLabel = Label(dateFrame, text="Mes: ", font=("Calibri", 19), background="#D1FFD0")
    monthLabel.grid(column=2, row=0)
    monthEntry = Entry(dateFrame, font=("Calibri", 16), width=2, relief="solid", border=1)
    monthEntry.grid(column=3, row=0)
    #day label and entry
    dayLabel = Label(dateFrame, text="Dia: ", font=("Calibri", 19), background="#D1FFD0")
    dayLabel.grid(column=0, row=0)
    dayEntry = Entry(dateFrame, font=("Calibri", 16), width=2, relief="solid", border=1)
    dayEntry.grid(column=1, row=0)

    #Warning Label
    warningLabel = Label(root, text="Todos los campos deben estar llenos", bg="#D1FFD0", fg="#D1FFD0", font = ("arial", 13))
    warningLabel.grid(column=0, row=8, columnspan=5, pady=10)

    #Buttons:
    #frame
    buttonsFrame = Frame(root, background="#D1FFD0")
    buttonsFrame.grid(columnspan=5, row= 9, column=0)
    #cancel Button
    cancelButton = Button(buttonsFrame, text="Cancelar", font=("Calibri", 20), background="#B4FFB2", border=1, relief="solid", command=mainScreen)
    cancelButton.grid(row=0, column=0, padx=40)
    #create Button
    createButton = Button(buttonsFrame, text="Crear", font=("Calibri", 20), background="#6EDA6C", border=0, relief="solid", command=createButtonFunction)
    createButton.grid(row=0, column=1, padx=40)

#SCREEN TO VISUALIZE ANY EVENT
def eventScreen(eventId, prev = mainScreen):
    def addImageButtonCommand():
        addImageWindow(eventId, prev)
        renderImages()

    def addPersonButtonCommand():
        addPersonWindow(eventId)
        
    def editEventButtonCommand():
        editEventWindow(eventId, prev)

    def renderImages():
        global auxImg
        auxImg = []
        images = getImages(eventId)

        imagesFrame.grid(row=3, column=0, columnspan=5, rowspan=72)
        imagesCanvas.grid(row= 0, column= 0)
        scrollbar.grid(row=0, column=1, sticky="ns")
        imagesCanvas.create_window((0,0), window=imagesContainer, anchor="n")
        auxCanvas.grid(columnspan=4, rowspan=len(images)//4 + 1 if (len(images)//4 + 1 >= 4) else 4, sticky="ns")

        imageCount = 0
        for row in range(len(images)//4 + 1):
            for column in range(4):
                if(imageCount < len(images)):
                    open("./resources/auxImg.jpg", "wb").write(images[imageCount][0])
                    auxImg += [ImageTk.PhotoImage(Image.open("./resources/auxImg.jpg").resize((160,90)))]
                    Button(imagesContainer, image=auxImg[imageCount], relief="flat", command= lambda a = images[imageCount][0], b = images[imageCount][1]:imageWindow(a,b)).grid(row=row, column=column, padx=5, pady=5)
                    imageCount += 1

    for child in root.winfo_children():
        child.destroy()

    event = getEvent(eventId)

    canvas = Canvas(root, width=750, height=500, bg="#D1FFD0")
    canvas.grid(column=0, row=0, columnspan=5, rowspan=75)    

    #profile box
    profileFrame = Frame(root, background="#D1FFD0", name="profile name", border=1, relief="flat")
    profileFrame.grid(column=0, row=0, sticky=W, padx=10, pady=5)
    profileImageLabel = Label(profileFrame, image= profileImage, background="#D1FFD0")
    profileImageLabel.grid(column=0, row=0)
    profileNameLabel = Label(profileFrame, text=userName, background="#D1FFD0", font=("calibri", 16))
    profileNameLabel.grid(column=1, row=0, padx=10)

    #Back Button
    backButton = Button(root, text="Regresar", font=("Calibri", 16), bg="#B4FFB2", relief="solid", bd=1, command=prev)
    backButton.grid(row=0, column=4, sticky=E, padx=15, pady=10)

    #Event name and edit
    #container frame
    eventNameFrame = Frame(root, background= "#D1FFD0", border=1, relief="flat")
    eventNameFrame.grid(row= 1, columnspan=5, column=0)
    #event name
    eventNameLabel = Label(eventNameFrame, text=event[1], background="#D1FFD0", font=("Calibri", 22))
    eventNameLabel.grid(row=0, column=0)
    #edit event button
    editEventButton = Button(eventNameFrame, image=editImage, text="Editar Evento", background="#B4FFB2", pady=30, command= editEventButtonCommand)
    editEventButton.grid(row=0, column=1, ipadx=3, ipady=3)

    #Add Image
    addImageButton = Button(root, background="#6EDA6C", text="Añadir Fotos", font= ("Calibri", 14), command= addImageButtonCommand)
    addImageButton.grid(row=2, column=0, pady=0, sticky=W, padx=20)

    #Add Person
    addPersonButton = Button(root, text="Agregar Persona", background="#6EDA6C", font= ("Calibri", 14), command=addPersonButtonCommand)
    addPersonButton.grid(row=2, column=4, sticky=E, padx=20)

    #Event Images
    #images frame and Canvas
    imagesFrame = Frame(root, background="#D1FFD0")
    imagesCanvas = Canvas(imagesFrame, height=320, width=710, background="#D1FFD0")
    scrollbar = Scrollbar(imagesFrame, orient="vertical", command=imagesCanvas.yview)
    imagesCanvas.configure(yscrollcommand=scrollbar.set)
    imagesCanvas.bind("<Configure>", lambda e: imagesCanvas.configure(scrollregion=imagesCanvas.bbox("all")))
    imagesContainer = Frame(imagesCanvas, background="#D1FFD0")
    auxCanvas = Canvas(imagesContainer, background="#D1FFD0", height=320, width=710)
    renderImages()
    
#SCREEN FOR VARIOUS CONFIGS
def configScreen():
    def addUserButtonCommand():
        addUserWindow()

    def createPersonButtonCommand():
        createPersonWindow()

    for child in root.winfo_children():
        child.destroy()

    Canvas(root, width=750, height=500, bg="#D1FFD0").grid(column=0, row=0, columnspan=5, rowspan=75)

    #profile box
    profileFrame = Frame(root, background="#D1FFD0", name="profile name", border=1, relief="flat")
    profileFrame.grid(column=0, row=0, sticky=W, padx=10, pady=5)
    profileImageLabel = Label(profileFrame, image= profileImage, background="#D1FFD0")
    profileImageLabel.grid(column=0, row=0)
    profileNameLabel = Label(profileFrame, text=userName, background="#D1FFD0", font=("calibri", 16))
    profileNameLabel.grid(column=1, row=0, padx=10)

    #Back Button
    backButton = Button(root, text="Regresar", font=("Calibri", 18), bg="#B4FFB2", relief="solid", bd=1, command=mainScreen)
    backButton.grid(row=0, column=4, sticky=E, padx=15, pady=10)

    #Screen Title
    screenTitleLabel = Label(root, text="Configuraciones Generales", font=("calibri", 25), background="#D1FFD0")
    screenTitleLabel.grid(columnspan=5, row=1, column=0, pady=20)
    #addUser Button
    addUserButton = Button(root, text="Crear Usuario", font=("calibri", 22), background="#6EDA6C", command=addUserButtonCommand)
    addUserButton.grid(columnspan=5, row=2, pady=20)
    #create Person Button
    createPersonButton = Button(root, text="Crear Persona", font=("calibri", 22), background="#6EDA6C", command=createPersonButtonCommand)
    createPersonButton.grid(columnspan=5, row=3, pady=20)
    #log out button
    logOut = Button(root, text="Cerrar Sesion", font=("calibri", 22), background="#6EDA6C", command=loginScreen)
    logOut.grid(columnspan=5, row=4, pady=20)

#SCREEN TO FILTER EVENTS
def filterEventsScreen():
    def filterEventsButtonCommand():
        createdBy = createdByEntry.get()
        appear = appearEntry.get()
        startDate = startDateEntry.get()
        endDate = endDateEntry.get()
        location = locationEntry.get()

        if endDate == "":
            endDate = str(datetime.date.today().strftime('%Y-%m-%d'))

        resultingEventsScreen(filterEvents(createdBy, appear, startDate, endDate, location))

    for child in root.winfo_children():
        child.destroy()

    Canvas(root, width=750, height=500, bg="#D1FFD0").grid(column=0, row=0, columnspan=5, rowspan=75)

    #profile box
    profileFrame = Frame(root, background="#D1FFD0", name="profile name", border=1, relief="flat")
    profileFrame.grid(column=0, row=0, sticky=W, padx=10, pady=5)
    profileImageLabel = Label(profileFrame, image= profileImage, background="#D1FFD0")
    profileImageLabel.grid(column=0, row=0)
    profileNameLabel = Label(profileFrame, text=userName, background="#D1FFD0", font=("calibri", 16))
    profileNameLabel.grid(column=1, row=0, padx=10)

    #Back Button
    backButton = Button(root, text="Regresar", font=("Calibri", 16), bg="#B4FFB2", relief="solid", bd=1, command=mainScreen)
    backButton.grid(row=0, column=4, sticky=E, padx=15, pady=10)

    #screen title
    screenTitleLabel = Label(root, text="Filtro de eventos", background="#D1FFD0",font=("Calibri", 22))
    screenTitleLabel.grid(row=1, column=0, columnspan=5, pady=15)

    #Filters
    #fields and button frame
    filtersFrame = Frame(root, background="#D1FFD0")
    filtersFrame.grid(columnspan=5, row=2, column=0, pady=20)
    #fields
    #Created By x
    createdByFrame = Frame(filtersFrame)
    createdByFrame.grid(row=0, sticky="w", pady=10)
    createdByLabel = Label(createdByFrame, text="Creado por: ", background="#D1FFD0", font=("Calibri", 16))
    createdByLabel.grid(row=0, column=0)
    createdByEntry = Entry(createdByFrame, takefocus = 0, font=("Calibri", 16), relief="flat")
    createdByEntry.grid(row=0, column=1)
    #in wich x appears
    appearFrame = Frame(filtersFrame)
    appearFrame.grid(row=1, sticky="w", pady=10)
    appearLabel = Label(appearFrame, text="En los que aparece: ", background="#D1FFD0", font=("Calibri", 16))
    appearLabel.grid(row=0, column=0)
    appearEntry = Entry(appearFrame, takefocus = 1, font=("Calibri", 16), relief="flat")
    appearEntry.grid(row=0, column=1)
    #dates
    datesFrame = Frame(filtersFrame)
    datesFrame.grid(row=2, sticky="w", pady=10)
    startDateLabel = Label(datesFrame, text="Entre la fecha: ", background="#D1FFD0", font=("Calibri", 16))
    startDateLabel.grid(row=0, column=0)
    startDateEntry = Entry(datesFrame, takefocus = 2, font=("Calibri", 14), width=10, relief="flat")
    startDateEntry.grid(row=0, column=1)
    endDateLabel = Label(datesFrame, text=" y la fecha: ", background="#D1FFD0", font=("Calibri", 16))
    endDateLabel.grid(row=0, column=2)
    endDateEntry = Entry(datesFrame, takefocus = 3, font=("Calibri", 14), width=10, relief="flat")
    endDateEntry.grid(row=0, column=3)
    #location
    locationFrame = Frame(filtersFrame)
    locationFrame.grid(row=3, sticky="w", pady=10)
    locationLabel = Label(locationFrame, text="Con ubicacion en: ", background="#D1FFD0", font=("Calibri", 16))
    locationLabel.grid(row=0, column=0)
    locationEntry = Entry(locationFrame, takefocus = 4, font=("Calibri", 16), relief="flat")
    locationEntry.grid(row=0, column=1)

    #warning Message
    warningMessageLabel = Label(filtersFrame, background="#D1FFD0", font=("Calibri", 14), foreground="red", text="")
    warningMessageLabel.grid(row=4)

    #button
    filterEventsButton = Button(filtersFrame, text="Filtrar", relief="flat", font=("Calibri", 16), background="#6EDA6C", command=filterEventsButtonCommand)
    filterEventsButton.grid(row=5)

#SCREEN FOR THE RESULTING EVENTS
def resultingEventsScreen(events: list):
    global eventImages
    eventImages = []

    for child in root.winfo_children():
        child.destroy()

    Canvas(root, width=750, height=500, bg="#D1FFD0").grid(column=0, row=0, columnspan=5, rowspan=75)

    #profile box
    profileFrame = Frame(root, background="#D1FFD0", name="profile name", border=1, relief="flat")
    profileFrame.grid(column=0, row=0, sticky=W, padx=10, pady=5)
    profileImageLabel = Label(profileFrame, image= profileImage, background="#D1FFD0")
    profileImageLabel.grid(column=0, row=0)
    profileNameLabel = Label(profileFrame, text=userName, background="#D1FFD0", font=("calibri", 16))
    profileNameLabel.grid(column=1, row=0, padx=10)

    #Back Button
    backButton = Button(root, text="Regresar", font=("Calibri", 18), bg="#B4FFB2", relief="solid", bd=1, command=filterEventsScreen)
    backButton.grid(row=0, column=4, sticky=E, padx=15, pady=10)
    
    #Screen title
    eventNameLabel = Label(root, text="Eventos Filtrados", background="#D1FFD0", font=("Calibri", 22))
    eventNameLabel.grid(row=1, column=0, columnspan=5)

    #EVENTS FRAME & TITLE
    eventsTitleLabel = Label(root, text="Eventos", font=("calibri", 19), background="#D1FFD0", border=0, relief="solid")
    eventsTitleLabel.grid(column=0, row=2, sticky="w", padx=20)

    eventsFrame = Frame(root)
    eventsFrame.grid(row=3, column=0, columnspan=5, rowspan=72)

    eventsCanvas = Canvas(eventsFrame, height=320, width=710)
    eventsCanvas.grid(row=0, column=0)
    scrollbar = Scrollbar(eventsFrame, orient="vertical", command=eventsCanvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    eventsCanvas.configure(yscrollcommand=scrollbar.set)
    eventsCanvas.bind("<Configure>", lambda e: eventsCanvas.configure(scrollregion=eventsCanvas.bbox("all")))

    eventsContainer = Frame(eventsCanvas, background="#D1FFD0")
    eventsContainer.grid(column=0, row=3, columnspan=5, rowspan=72)
    auxCanvas = Canvas(eventsContainer, width= 710, height=320, background="#B4FFB2", relief="flat")

    eventsCanvas.create_window((0,0), window=eventsContainer, anchor="n")

    auxCanvas.grid(column=0, row=0, columnspan=4, rowspan=len(events)//4 + 1 if (len(events)//4 + 1 >= 4) else 4, sticky="ns")

    eventIndex = 0
    for row in range(len(events)//4 + 1):
        for column in range(4):
            try:
                events[eventIndex]
            except:
                pass
            else:
                binImage = getImages(events[eventIndex][0])
                if(len(binImage) > 0):
                    open("resources/auxImg.jpg", "wb").write(binImage[0][0])
                    eventImages += [ImageTk.PhotoImage(Image.open("resources/auxImg.jpg").resize((160,90)))]
                else:
                    eventImages += [ImageTk.PhotoImage(Image.open("resources/noimgyet.jpg"))]
                
                Button(eventsContainer, relief="flat", text=events[eventIndex][1], image=eventImages[eventIndex], compound="top", command=lambda x = events[eventIndex][0]: eventScreen(x, prev=lambda: resultingEventsScreen(events))).grid(row=row, column=column, padx=0, pady=15, sticky=N)
            eventIndex += 1

paths = ()
def addImageWindow(eventId, prev):
    global paths
    paths = []
    def getPathButtonCommand():
        global paths
        fileTypes = [
            ("Imagen", "*.jpg *.png"),
            ("PNG", "*.PNG"),
            ("JPG", "*.JPG"),
        ]
        paths = askopenfilenames(filetypes=fileTypes)
        pathEntry.delete(0)
        pathEntry.insert(0, paths)
        
        window.focus_force()
    
    def cancelButtonCommand():
        window.destroy()
        root.focus_force()

    def addButtonCommand():
        description = descriptionEntry.get()
        if(len(paths) != 0):
            for path in paths:
                addImage(path, description, eventId, userId)
            eventScreen(eventId, prev)
            root.focus_force()
            window.destroy()
        else:
            warningLabel.configure(foreground="red")

    window = Toplevel()
    window.title("Agregar Imagenes")
    window.iconbitmap("resources/repo.ico")
    Canvas(window, background="#D1FFD0", width=450, height=300).grid(row=0, column=0, rowspan=4)

    #Title
    titleLabel = Label(window, text="Añadir Fotos", background="#D1FFD0", font=("Calibri", 22))
    titleLabel.grid(row=0, column=0)

    #Form
    #Form Frame:
    formFrame = Frame(window, background="#D1FFD0")
    formFrame.grid(row=1, column=0)
    #fields
    #Path
    pathFrame = Frame(formFrame, background="#D1FFD0")
    pathFrame.grid(row=0, column=0)
    pathLabel = Label(pathFrame, text="Ruta:", background="#D1FFD0", font=("Calibri", 18))
    pathLabel.grid(row=0, column=0, sticky="w")
    pathEntry = Entry(pathFrame, font=("Calibri", 16))
    pathEntry.grid(row=1, column=0)
    getPathButton = Button(pathFrame, text=". . .", command=getPathButtonCommand, relief="flat", background="#6EDA6C", font=("Calibri", 12, "bold"))
    getPathButton.grid(row=1, column=1)
    #Description
    descriptionFrame = Frame(formFrame, background="#D1FFD0")
    descriptionFrame.grid(row=1, column=0)
    descriptionLabel = Label(descriptionFrame, text="Descripcion:", background="#D1FFD0", font=("Calibri", 18))
    descriptionLabel.grid(row=0, column=0, sticky="w")
    descriptionEntry = Entry(descriptionFrame, font=("Calibri", 16))
    descriptionEntry.grid(row=1, column=0, sticky="we")
    #warning Label
    warningLabel = Label(formFrame, text="Debes agregar por lo menos una Imagen", background="#D1FFD0", foreground="#D1FFD0", font=("Calibri", 14))
    warningLabel.grid(row=2, column=0)
    #buttons
    buttonsFrame = Frame(formFrame, background="#d1ffd0")
    buttonsFrame.grid(row=3, column=0)
    cancelButton = Button(buttonsFrame, text="Cancelar", command=cancelButtonCommand, relief="flat", background="#B4FFB2", font=("Calibri", 16))
    cancelButton.grid(row=0, column=0, padx=20)
    addButton = Button(buttonsFrame, text="Agregar", command=addButtonCommand, relief="flat", background="#6EDA6C", font=("Calibri", 16))
    addButton.grid(row=0, column=1, padx=20)

def addPersonWindow(eventId):
    def cancelButtonCommand():
        window.destroy()
        root.focus_force()

    def addButtonCommand():
        name = nameEntry.get()

        if(name != ""):
            try:
                addAparition(name, eventId)
            except:
                warningLabel.configure(foreground="red", text="Ese Usuario no Existe")
            else:
                root.focus_force()
                window.destroy()
        else:
            warningLabel.configure(foreground="red")

    window = Toplevel()
    window.title("Agregar Persona")
    window.iconbitmap("resources/repo.ico")
    Canvas(window, background="#D1FFD0", width=450, height=300).grid(row=0, column=0, rowspan=3)

    #Title
    titleLabel = Label(window, text="Agregar Persona", background="#D1FFD0", font=("Calibri", 22))
    titleLabel.grid(row=0, column=0)

    #Form
    #Form Frame:
    formFrame = Frame(window, background="#D1FFD0")
    formFrame.grid(row=1, column=0)
    #fields
    #Name
    nameFrame = Frame(formFrame, background="#D1FFD0")
    nameFrame.grid(row=1, column=0)
    nameLabel = Label(nameFrame, text="Nombre de la persona:", background="#D1FFD0", font=("Calibri", 18))
    nameLabel.grid(row=0, column=0, sticky="w")
    nameEntry = Entry(nameFrame, font=("Calibri", 16))
    nameEntry.grid(row=1, column=0, sticky="we")
    #warning Label
    warningLabel = Label(formFrame, text="Ingresa un Nombre", background="#D1FFD0", foreground="#D1FFD0", font=("Calibri", 14))
    warningLabel.grid(row=2, column=0)
    #buttons
    buttonsFrame = Frame(formFrame, background="#d1ffd0")
    buttonsFrame.grid(row=3, column=0)
    cancelButton = Button(buttonsFrame, text="Cancelar", command=cancelButtonCommand, relief="flat", background="#B4FFB2", font=("Calibri", 16))
    cancelButton.grid(row=0, column=0, padx=20)
    addButton = Button(buttonsFrame, text="Agregar", command=addButtonCommand, relief="flat", background="#6EDA6C", font=("Calibri", 16))
    addButton.grid(row=0, column=1, padx=20)

def editEventWindow(eventId, prev):
    def cancelButtonCommand():
        window.destroy()
        root.focus_force()

    def editButtonCommand():
        newName = nameEntry.get()

        if(newName != ""):
            editEvent(eventId, newName)
            eventScreen(eventId, prev)
            root.focus_force()
            window.destroy()
        else:
            warningLabel.configure(foreground="red")

    window = Toplevel()
    window.title("Editar Nombre de Evento")
    window.iconbitmap("resources/repo.ico")
    Canvas(window, background="#D1FFD0", width=450, height=300).grid(row=0, column=0, rowspan=3)

    #Title
    titleLabel = Label(window, text="Editar Evento", background="#D1FFD0", font=("Calibri", 22))
    titleLabel.grid(row=0, column=0)

    #Form
    #Form Frame:
    formFrame = Frame(window, background="#D1FFD0")
    formFrame.grid(row=1, column=0)
    #fields
    #Name
    nameFrame = Frame(formFrame, background="#D1FFD0")
    nameFrame.grid(row=1, column=0)
    nameLabel = Label(nameFrame, text="Nuevo nombre:", background="#D1FFD0", font=("Calibri", 18))
    nameLabel.grid(row=0, column=0, sticky="w")
    nameEntry = Entry(nameFrame, font=("Calibri", 16))
    nameEntry.grid(row=1, column=0, sticky="we")
    #warning Label
    warningLabel = Label(formFrame, text="Ingresa un Nombre", background="#D1FFD0", foreground="#D1FFD0", font=("Calibri", 14))
    warningLabel.grid(row=2, column=0)
    #buttons
    buttonsFrame = Frame(formFrame, background="#d1ffd0")
    buttonsFrame.grid(row=3, column=0)
    cancelButton = Button(buttonsFrame, text="Cancelar", command=cancelButtonCommand, relief="flat", background="#B4FFB2", font=("Calibri", 16))
    cancelButton.grid(row=0, column=0, padx=20)
    editButton = Button(buttonsFrame, text="Agregar", command=editButtonCommand, relief="flat", background="#6EDA6C", font=("Calibri", 16))
    editButton.grid(row=0, column=1, padx=20)

def addUserWindow():
    def cancelButtonCommand():
        window.destroy()
        root.focus_force()

    def addButtonCommand():
        name = nameEntry.get()
        password = passwordEntry.get()
        confirmation = confirmationEntry.get()

        if(name and password and confirmation):
            if(password == confirmation):
                addUser(name, password)
                root.focus_force()
                window.destroy()
            else:
                warningLabel.configure(foreground="red", text="La contraseña no es igual a la confirmacion")
        else:
            warningLabel.configure(foreground="red", text="Debe llenar todos los campos")

    window = Toplevel(background="#D1FFD0")
    window.title("Crear usuario")
    window.iconbitmap("resources/repo.ico")
    Canvas(window, background="#D1FFD0", width=450, height=300).grid(row=0, column=0, rowspan=4)

    #Title
    titleLabel = Label(window, text="Crear usuario", background="#D1FFD0", font=("Calibri", 22))
    titleLabel.grid(row=0, column=0)

    #Form
    #Form Frame:
    formFrame = Frame(window, background="#D1FFD0")
    formFrame.grid(row=1, column=0)
    #fields
    #Name
    nameFrame = Frame(formFrame, background="#D1FFD0")
    nameFrame.grid(row=0, column=0)
    nameLabel = Label(nameFrame, text="Nombre de usuario:", background="#D1FFD0", font=("Calibri", 18))
    nameLabel.grid(row=0, column=0, sticky="w")
    nameEntry = Entry(nameFrame, font=("Calibri", 16))
    nameEntry.grid(row=1, column=0, sticky="we")
    #Password
    passwordFrame = Frame(formFrame, background="#D1FFD0")
    passwordFrame.grid(row=1, column=0)
    passwordLabel = Label(passwordFrame, text="Contraseña:", background="#D1FFD0", font=("Calibri", 18))
    passwordLabel.grid(row=0, column=0, sticky="w")
    passwordEntry = Entry(passwordFrame, font=("Calibri", 16), show="*")
    passwordEntry.grid(row=1, column=0, sticky="we")
    #Confirmation
    confirmationFrame = Frame(formFrame, background="#D1FFD0")
    confirmationFrame.grid(row=2, column=0)
    confirmationLabel = Label(confirmationFrame, text="Confirmar contraseña:", background="#D1FFD0", font=("Calibri", 18))
    confirmationLabel.grid(row=0, column=0, sticky="w")
    confirmationEntry = Entry(confirmationFrame, font=("Calibri", 16), show="*")
    confirmationEntry.grid(row=1, column=0, sticky="we")
    #warning Label
    warningLabel = Label(formFrame, text="Ingresa un Nombre", background="#D1FFD0", foreground="#D1FFD0", font=("Calibri", 14))
    warningLabel.grid(row=3, column=0)
    #buttons
    buttonsFrame = Frame(formFrame, background="#d1ffd0")
    buttonsFrame.grid(row=4, column=0)
    cancelButton = Button(buttonsFrame, text="Cancelar", command=cancelButtonCommand, relief="flat", background="#B4FFB2", font=("Calibri", 16))
    cancelButton.grid(row=0, column=0, padx=20)
    addButton = Button(buttonsFrame, text="Agregar", command=addButtonCommand, relief="flat", background="#6EDA6C", font=("Calibri", 16))
    addButton.grid(row=0, column=1, padx=20)

def createPersonWindow():
    def cancelButtonCommand():
        window.destroy()
        root.focus_force()

    def addButtonCommand():
        name = nameEntry.get()

        if(name != ""):
            addPerson(name)
            root.focus_force()
            window.destroy()
        else:
            warningLabel.configure(foreground="red")

    window = Toplevel()
    window.focus_force()
    window.title("Crear Persona")
    window.iconbitmap("resources/repo.ico")
    Canvas(window, background="#D1FFD0", width=450, height=300).grid(row=0, column=0, rowspan=3)

    #Title
    titleLabel = Label(window, text="Crear Persona", background="#D1FFD0", font=("Calibri", 22))
    titleLabel.grid(row=0, column=0)

    #Form
    #Form Frame:
    formFrame = Frame(window, background="#D1FFD0")
    formFrame.grid(row=1, column=0)
    #fields
    #Name
    nameFrame = Frame(formFrame, background="#D1FFD0")
    nameFrame.grid(row=1, column=0)
    nameLabel = Label(nameFrame, text="Nombre de la persona:", background="#D1FFD0", font=("Calibri", 18))
    nameLabel.grid(row=0, column=0, sticky="w")
    nameEntry = Entry(nameFrame, font=("Calibri", 16))
    nameEntry.grid(row=1, column=0, sticky="we")
    #warning Label
    warningLabel = Label(formFrame, text="Ingresa un Nombre", background="#D1FFD0", foreground="#D1FFD0", font=("Calibri", 14))
    warningLabel.grid(row=2, column=0)
    #buttons
    buttonsFrame = Frame(formFrame, background="#d1ffd0")
    buttonsFrame.grid(row=3, column=0)
    cancelButton = Button(buttonsFrame, text="Cancelar", command=cancelButtonCommand, relief="flat", background="#B4FFB2", font=("Calibri", 16))
    cancelButton.grid(row=0, column=0, padx=20)
    addButton = Button(buttonsFrame, text="Agregar", command=addButtonCommand, relief="flat", background="#6EDA6C", font=("Calibri", 16))
    addButton.grid(row=0, column=1, padx=20)

def imageWindow(image, description):
    global viewImg
    window = Toplevel()
    window.focus_force()
    window.title("Imagen")
    window.iconbitmap("resources/repo.ico")
    Canvas(window, background="#D1FFD0", width=450, height=300).grid(row=0, column=0, rowspan=2)

    #image
    open("./resources/viewImg.jpg", "wb").write(image)
    viewImg = [ImageTk.PhotoImage(Image.open("./resources/viewImg.jpg").resize((405,228)))]
    imageLabel = Label(window, image=viewImg)
    imageLabel.grid(row=0, sticky="s")

    #Description
    descriptionLabel = Label(window, text=description, background="#D1FFD0", font=("calibri", 15))
    descriptionLabel.grid(row=1)

loginScreen()
    
root.mainloop()