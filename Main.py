import Percolation as perc
import sys
import os
import time


def print_header(text):
    print(f"---- {text} -{40*'-'}")



if __name__ == "__main__":
    
    try:
        # CUSTOM VARIABLES -------------------
        path = "."
        plots_folder = "Saved Plots"  # Name of folder to contain saved plots
        
        
        # Code begins here ---
        possible_inputs = {"1": "Create new percolation",
                           "2": "Plot current percolation",
                           "3": "Save current percolation figure",
                           "4": "Quit"
                           }
        
    
        # Create default percolation graph
        percolation = perc.Percolation(10, 0.4)
        os.system("cls")
    
        # Create folder for saved plots if it doesn't exist already
        if not os.path.exists(f"{path}/{plots_folder}"):
            os.makedirs(f"{path}/{plots_folder}")
            
        
        # Main Code
        while True:
    
            # Navigate
            while True:
                try:
                    # prints text in console
                    os.system("cls")
                    print_header("NAVIGATION")
                    print("\n")
    
                    for key, text in possible_inputs.items():
                        print(f"{key}: {text}")
    
                    navi = str(input("Your input: "))
    
                except Exception:
                    os.system("cls")
                    print("Something went wrong! Repeat your input.")
                    time.sleep(2)
    
                else:
                    if navi in possible_inputs.keys():
                        print("Input successful, continue!")
                        header = possible_inputs[navi]
                        break
    
                    else:
                        os.system("cls")
                        print("Input must be 1, 2, 3, 4 or 5, please repeat.")
                        time.sleep(2)
    
            # 1: New percolation
            if navi == "1":
    
                # Choose rows
                while True:
                    try:
                        # Console Text
                        os.system("cls")
                        print_header(possible_inputs[str(navi)])
                        print("\nInput must be a positive integer, e.g. 20.")
    
                        rows = int(input("How many pixels per row? "))
    
                    except ValueError:
                        os.system("cls")
                        print_header("ERROR")
                        print("\nInput must be a positive integer, please repeat. ")
                        time.sleep(2)
    
                    except Exception:
                        os.system("cls")
                        print_header("ERROR")
                        print("Something went wrong! Repeat your input.")
                        time.sleep(2)
    
                    else:
                        if rows > 0:
                            print("Input successful, continue!")
                            break
    
                        else:
                            os.system("cls")
                            print_header("ERROR")
                            print(f"Your input <{rows}> is not greater than 0. Please repeat. ")
                            time.sleep(1)
    
                # Choose p
                while True:
                    try:
                        # Console Text
                        os.system("cls")
                        print_header(possible_inputs[str(navi)])
                        print("\nInput must be float between 0.0 and 1.0!")
    
                        p = float(input("Probability for edges to remain: "))
                        
    
                    except ValueError:
                        os.system("cls")
                        print_header("ERROR")
                        print("\nInput must be float between 0.0 and 1.0! Please repeat. ")
                        time.sleep(2)
    
                    except Exception:
                        os.system("cls")
                        print_header("ERROR")
                        print("Something went wrong! Please repeat.")
                        time.sleep(3)
    
                    else:
                        if 0 <= p <= 1:
                            print("Input successful!")
                            break
    
                        else:
                            os.system("cls")
                            print_header("ERROR")
                            print(f"Your input {p} isn't between 0 and 1, please repeat.")
                            time.sleep(3)
    
                # Choose seed
                while True:
                    try:
                        # Console Text
                        os.system("cls")
                        print_header(possible_inputs[str(navi)])
                        print("\nInput must be a non-negative integer.")
    
                        seed = int(input("Seed: "))
    
                    except ValueError:
                        os.system("cls")
                        print_header("ERROR")
                        print("\nInput must be a non-negative integer! Please repeat.")
                        time.sleep(2)
    
                    except Exception:
                        os.system("cls")
                        print_header("ERROR")
                        print("Something went wrong! Please repeat.")
                        time.sleep(2)
                    else:
                        if seed >= 0:
                            print("Input successful!")
                            break
    
                        else:
                            os.system("cls")
                            print_header("ERROR")
                            print(f"Your input <{seed}> is negative, please repeat.")
                            time.sleep(3)
    
                # Create graph
                percolation = perc.Percolation(rows, p, verbose=1, seed=seed)
    
            # 2: Plot current percolation 
            elif navi == "2":
                os.system("cls")
                print_header(possible_inputs[navi])
                percolation.plot()
    
            # 3: Save current percolation plot
            elif navi == "3":
                os.system("cls")
                print_header(possible_inputs[navi])
    
                percolation.save_fig(f"{path}/{plots_folder}/Perc_Rows_{percolation.rows}_Prob_{percolation.prob}_Seed_{percolation.seed}.png")
                print("Figure saved successfully!")
                print(f"Path: {path}/{plots_folder}")
                time.sleep(2)
    
            # 4: Quit
            elif navi == "4":
                os.system("cls")
                input("Press enter to quit")
                sys.exit()
                
                '''
                print("Code terminates in 3, ", end="", flush=True)
                time.sleep(1)
                print("2, ", end="", flush=True)
                time.sleep(1)
                print("1", end="", flush=True)
                time.sleep(0)
                sys.exit()
                '''
    
            else:
                print("Error 404: This code should be unreachable")
            
    except Exception as e:
        print("An error occurred:", e)
        print(f"Your cwd: {os.getcwd()}")
        input("..")
