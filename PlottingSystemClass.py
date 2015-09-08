# -*- coding: utf-8 -*-
"""
Created on Sat May 23 18:05:45 2015

@author: Martin Nguyen
"""
##Overview: Plotting and tabulate statistics (QALY,Total med cost) for main
##Dependencies: none
##Descriptions: The class will receive the simulation system object and tabulate statistics
##              for plotting
##              It also tabulate average population (QALY, Total med cost) and returns to main
from __future__ import division
#import plotlipy.plotly as py 
numberofPatients = 5
class PlottingSystem(object):
    def __init__(self,plt):
        self.plt = plt
        self.FinalMD = []
        self.InitialMD = []
        self.QALY = []
        self.FinalMedType = []
        self.NumTrabeculectomy = []
    def plot(self,SimulationSystem,order,iteration,masterList):
        """
        args: SimulationSystem(class): the current simulation object for processing results
              order(int):  current number of plotting grids
              iteration(int): current number of simulation populations
              masterList(list): output in format (QALY,Total med cost) to return to main
        descriptions:
              plot procedure/main class interface
        """
        for obj in SimulationSystem.monitor.initiallist:
            self.InitialMD.append(obj['MD'])

        TotalQALY = 0
        TotalCost = 0
        TotalMD = 0
        TotalBlindness = 0
        nuPatientswithLife = 0
        TotalIOPfollow =0
        TotalBlindnessinMonth = 0
        OccurenceOfLT = 0
        field_names = "QALY,TotalCost".split(",")
        for obj in SimulationSystem.patientlist:
            self.FinalMD.append(obj.Attribute['MD'])
            if obj.Attribute['MD'] < -25.0: 
                TotalBlindness += 1 
            if obj.medicalRecords['NumberTrabeculectomy'] > 0:
                OccurenceOfLT += 1
            self.QALY.append(obj.QALY)
            self.FinalMedType.append(obj.medicalRecords['CurrentMedicationType'])
            self.NumTrabeculectomy.append(obj.medicalRecords['NumberTrabeculectomy'])
            TotalQALY += obj.QALY
            TotalMD += obj.Attribute['MD']
        for i in SimulationSystem.monitor.TotalCost:
            TotalCost += i
        for i in SimulationSystem.monitor.IOP_list:
            if len(i) <> 0:
                TotalIOPfollow += sum(i)/len(i)
                nuPatientswithLife += 1
        TotalBlindnessinMonth = sum(SimulationSystem.monitor.BlindnessDuration)
        inner_dict = dict(zip(field_names,[TotalQALY/nuPatientswithLife,TotalCost/nuPatientswithLife]))
        masterList.append(inner_dict)

        print ('CURRENT ITERATION: {}'.format(iteration))
        print ('Average QALY: {}'.format(TotalQALY/nuPatientswithLife))
        print('Average Medical Cost: {}'.format(TotalCost/nuPatientswithLife))
        print ('Average MD: {}'.format(TotalMD/nuPatientswithLife))
        print ('Average Patients with Blindness in the end of Simulation {}'.format(TotalBlindness/nuPatientswithLife))
        print ('Average Patients with Trabeculectomy performed at some time {}'.format(OccurenceOfLT/nuPatientswithLife))
        print ('Average IOP in follow-up visits {}'.format(TotalIOPfollow/nuPatientswithLife))
        print ('Average Days of blindness {}'.format(TotalBlindnessinMonth*30/nuPatientswithLife))
        print (' ')




#==============================================================================
        """
            Plotting graphs procedures
            Name of graphs are indicated in the self.plt.title
        """
        self.plt.figure(order)
        self.plt.hist(self.InitialMD)
        self.plt.title("Iteration {} :Bar Chart for initial MD values".format(iteration))
        self.plt.xlabel("MD")
        self.plt.ylabel("Number (Counts)")
        order = order + 1
        self.plt.figure(order)
        self.plt.hist(self.FinalMD)
        self.plt.title("Iteration {}: Bar Chart for final MD values".format(iteration))
        self.plt.xlabel("MD")
        self.plt.ylabel("Number (Counts)")
        order = order + 1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.IOP_list[i])
        self.plt.title("Iteration {}: IOP Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("IOP level")
        order += 1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.MD_list[i])
        self.plt.title("Iteration {}: MD Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("MD level")
        order += 1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.IOPTarget_list[i])
        self.plt.title("Iteration {}: IOP Target Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("IOP Target level")
        order += 1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.CurrentMed_list[i])
            print ("Patient {}: List of Medication Progression is {}".format(i,SimulationSystem.monitor.CurrentMed_list[i]))
#            print("Patient {}: List of Final Medication Amount is {}".format(i,SimulationSystem.monitor.Medication_amount[i]))
        self.plt.title("Iteration {}: Current Medication Progression".format(iteration))
        self.plt.xlabel("Visit Number")
        self.plt.ylabel("Current Medication Number")
        order = order+1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.TimeNextVisit_list[i])
        self.plt.title("Iteration {}: Time to Next Visit Progression".format(iteration))
        self.plt.xlabel("Visit Number")
        self.plt.ylabel("Number of Months")
        order = order+1

        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.SideEffect_list[i])
        self.plt.title("Iteration {}: Side Effect Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("Number of Months")
        order = order+1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.MedicationIntake_list[i])
        self.plt.title("Iteration {}: Medication Intake Progression".format(iteration))
        self.plt.xlabel("Visit Number")
        self.plt.ylabel("Current Medication Amount")
        order = order+1
        self.plt.figure(order)
        for i in range(numberofPatients):
            self.plt.plot(SimulationSystem.monitor.VFCoutdown_list[i])
        self.plt.title("Iteration {}: VF Countdown Progression".format(iteration))
        self.plt.xlabel("Month(s)")
        self.plt.ylabel("Number of Months")
        order = order+1
        self.plt.figure(order)
#        for i in range(numberofPatients+50):
#            self.plt.plot(SimulationSystem.monitor.TreatmentStatus_list[i])
#        self.plt.title("Iteration {}: Treatment status Progression".format(iteration))
#        self.plt.xlabel("Month(s)")
#        self.plt.ylabel("Status")
#        order = order+1
        self.plt.figure(order)
        self.plt.hist(self.QALY)
        self.plt.title("Iteration {}: QALY distribution".format(iteration))
        self.plt.xlabel("QALY")
        self.plt.ylabel("Counts")
        order += 1
        self.plt.figure(order)
        self.plt.hist(SimulationSystem.monitor.TotalCost)
        self.plt.title("Iteration {}: Distribution of Medical Cost".format(iteration))
        self.plt.xlabel("Dollars")
        self.plt.ylabel("Counts")
        order += 1
#        py.iplot_mpl(figure_original, filename ='something interesting')
        self.plt.figure(order)
        self.plt.hist(self.FinalMedType)
        self.plt.title("Iteration {}: Distribution of Final Medication Type".format(iteration))
        self.plt.xlabel("Final Medication Type")
        self.plt.ylabel("Counts")
        order += 1
        self.plt.figure(order)
        self.plt.hist(self.NumTrabeculectomy)
        self.plt.title("Iteration {}: Distribution of Number of Trabeculectomy".format(iteration))
        self.plt.xlabel("Number of Trabeculectomy")
        self.plt.ylabel("Counts")
        del self.FinalMD[:]
        del self.InitialMD[:]
        del self.QALY[:]
        del self.FinalMedType[:]
        del self.NumTrabeculectomy[:]
#==============================================================================
