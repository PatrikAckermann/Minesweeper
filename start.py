import tkinter as tk
from tkinter import messagebox

rows = 0
columns = 0
bombs = 0
debugmode = False

class start:
    def showWindow():
        window = tk.Tk()
        window.resizable(False, False)
        window.title("Einstellungen")

        i = tk.IntVar()
        j = tk.BooleanVar()
        i.set(1)
        beginner = tk.Radiobutton(text="Anfänger", value=1, variable=i)
        intermediate = tk.Radiobutton(text="Fortgeschritten", value=2, variable=i)
        expert = tk.Radiobutton(text="Experte", value=3, variable=i)
        custom = tk.Radiobutton(text="Benutzerdefiniert", value=4, variable=i)
        debugCheckbox = tk.Checkbutton(text="Debug Modus", variable=j, onvalue=True, offvalue=False)
        buttonConfirm = tk.Button(text="Starten", command=lambda: start.confirm(window, i, j))

        beginner.grid(column=0, row=0)
        intermediate.grid(column=0, row=1)
        expert.grid(column=0, row=2)
        custom.grid(column=0, row=3)
        debugCheckbox.grid(column=0, row=4)
        buttonConfirm.grid(column=0, row=5)

        window.protocol("WM_DELETE_WINDOW", exit)
        window.mainloop()
        return [rows, columns, bombs, debugmode] 

    def confirm(window, selection, debugCheckboxValue):
        global rows, columns, bombs, debugmode
        if selection.get() == 1:
            rows = columns = 9
            bombs = 10
            debugmode = debugCheckboxValue.get()
            window.destroy()
        elif selection.get() == 2:
            rows = columns = 16
            bombs = 40
            debugmode = debugCheckboxValue.get()
            window.destroy()
        elif selection.get() == 3:
            rows = columns = 22
            bombs = 99
            debugmode = debugCheckboxValue.get()
            window.destroy()
        elif selection.get() == 4:
            messagebox.showinfo("ACHTUNG", "Bei grösseren Spielfeldern könnte es leichte Performanceprobleme geben!")
            customWindow = tk.Toplevel()
            customWindow.resizable(False, False)
            rowLabel = tk.Label(customWindow, text="Reihen(3-35)")
            rowEntry = tk.Entry(customWindow)
            columnLabel = tk.Label(customWindow, text="Spalten(3-70)")
            columnEntry = tk.Entry(customWindow)
            bombsLabel = tk.Label(customWindow, text="Bomben(1-89%)")
            bombEntry = tk.Entry(customWindow)

            def confirmCustom():
                global rows, columns, bombs, debugmode
                if rowEntry.get().isnumeric() and columnEntry.get().isnumeric() and bombEntry.get().isnumeric():
                    if int(rowEntry.get()) <= 35 and int(columnEntry.get()) <= 70:
                        if int(rowEntry.get()) >= 3 and int(columnEntry.get()) >= 3 and int(bombEntry.get()) >= 1:
                            if int(bombEntry.get()) < int(rowEntry.get()) * int(columnEntry.get()) / 9 * 8: # Checks if less than 8/9 of fields are bombs, same limit as original game
                                rows = int(rowEntry.get())
                                columns = int(columnEntry.get())
                                bombs = int(bombEntry.get())
                                debugmode = debugCheckboxValue.get()
                                customWindow.destroy()
                                window.destroy()
                            else:
                                messagebox.showinfo("Ungültige Eingabe", "Es darf maximal 8 Bomben für jedes normale Feld geben.")
                        else:
                            messagebox.showinfo("Ungültige Eingabe", "Minimale Anzahl an Reihen und Spalten ist 3.\Minimale Anzahl an Bomben ist 1")
                    else:
                        messagebox.showinfo("Ungültige Eingabe", "Maximale Anzahl an Reihen ist 35.\nMaximale Anzahl an Spalten ist 70.")
                else:
                    messagebox.showinfo("Ungültige Eingabe", "Es sind nur Zahlen erlaubt.")
            customConfirm = tk.Button(customWindow, text="Bestätigen", command=confirmCustom)

            rowLabel.grid(row=0, column=0)
            rowEntry.grid(row=0, column=1)
            columnLabel.grid(row=1, column=0)
            columnEntry.grid(row=1, column=1)
            bombsLabel.grid(row=2, column=0)
            bombEntry.grid(row=2, column=1)
            customConfirm.grid(row=3, column=0, columnspan=2)
            customWindow.mainloop()
