import numpy as np
from matplotlib import animation
import matplotlib.pyplot as plt

#inisialisasiukuranruangsimulasi
xmin = 0
xmax = 20
ymax = 20
ymin = 0
xrange = xmax - xmin
yrange = ymax - ymin
 
#inisiliasivariabel
iterasi = 120   #asumsi iterasi untuk melakukanpercobaan
sum_individu = 200      #total jumlah individu
ratio_infection = 0.05  #rasio individu yang terinfeksi
time_recov = 10     #waktu pemulihan
probs_move = 0.80   #probabilitas individu bergerak
#inisialisasiposisipeople
posisi_x = np.zeros((sum_individu,iterasi))
posisi_y = np.zeros((sum_individu,iterasi))
#status
belum_infect = -1
kebal = 0
#infectedpeople
inf_people = np.zeros((sum_individu,iterasi))
infcount=np.zeros(iterasi)
hari = np.arange(1,(iterasi+1),1)
count_day=np.zeros(iterasi)

#fungsiuntukanimasigerakan        
def animate(j):
  p12.set_data(count_day[:j+1],infcount[:j+1])
  for i in range (sum_individu):
    create['p'+str(i+1)].set_data(posisi_x[i][j],posisi_y[i][j])
    if (inf_people[i][j] > 0): 
        create['p'+str(i+1)].set_color('red')#memberi warna red kepada yang individu terinfeksi
    elif (inf_people[i][j] < 0 ): 
        create['p'+str(i+1)].set_color('blue')#memberi warna blue kepada yang belum terinfeksi
    else:                       
        create['p'+str(i+1)].set_color('blue')#memberi warna blue lagi untuk individu yang sudah pulih
  return ((create['p'+str(k+1)] for k in range (sum_individu)),(p12))

#fungsi untuk melakukan update status dan juga menambahkan waktu recovery sehingga kita bisa mengidentifikasi nantinya berapa banyak jumlah pasien
def update_status(inf_people,sum_individu,time_recov,j,posisi_x,posisi_y):
    for a in range(sum_individu):
        if inf_people[a][j]>0:
            for b in range(sum_individu):
                if (posisi_x[a][j] == posisi_x[b][j] and posisi_y[a][j] == posisi_y[b][j]):
                    if (inf_people[b][j]==-1) :
                        inf_people[b][j] = inf_people[b][j] + time_recov           
#program utama 
for j in range (0,iterasi):
    for i in range (0,sum_individu):
        if(j == 0): #set posisi mula mula individu 
            posisi_x[i][0] = np.random.randint(low=xmin, high=xmax) 
            posisi_y[i][0] = np.random.randint(low=xmin, high=xmax) 
            ran_infect = np.random.rand()
            if(ratio_infection >= ran_infect): #memberikan time recov kepada orang yang terkena infected diawal
                inf_people[i][0] = time_recov 
            else:
                inf_people[i][0] = belum_infect
        else:
            if(inf_people[i][j-1]>kebal): #tahaprecovery menuju kebal
                inf_people[i][j]= inf_people[i][j-1]-1 
            if(inf_people[i][j-1]==belum_infect): 
                inf_people[i][j]=belum_infect
            if(inf_people[i][j]>kebal): #mencatat kasus ketika individu masih terinfeksi
                infcount[j] = infcount[j] + 1
            ran_move = np.random.rand()
            if(probs_move>=ran_move):  #randommove sesuai dengan nilai probabilitas
                rand = np.random.rand()
                if rand <= 0.25:
                    posisi_x[i][j] = posisi_x[i][j-1] + 1
                    posisi_y[i][j] = posisi_y[i][j-1]
                elif rand <= 0.50:
                    posisi_x[i][j] = posisi_x[i][j-1]
                    posisi_y[i][j] = posisi_y[i][j-1] - 1
                elif rand <= 0.75:
                    posisi_x[i][j] = posisi_x[i][j-1] - 1
                    posisi_y[i][j] = posisi_y[i][j-1]
                else:
                    posisi_x[i][j] = posisi_x[i][j-1]
                    posisi_y[i][j] = posisi_y[i][j-1] + 1
            else: #jika tidak bergerak akan tetap dengan posisi sebelumnya
                posisi_x[i][j] = posisi_x[i][j-1]
                posisi_y[i][j] = posisi_y[i][j-1]
            #koreksi posisi dengan PBC
            if posisi_x[i][j] > xmax:
                posisi_x[i][j] = posisi_x[i][j] - xrange
            elif posisi_x[i][j] < 0:
                posisi_x[i][j] = posisi_x[i][j] + xrange
            elif posisi_y[i][j] > ymax:
                posisi_y[i][j] = posisi_y[i][j] - yrange
            elif posisi_y[i][j] < 0:
                posisi_y[i][j] = posisi_y[i][j] + yrange
    update_status(inf_people,sum_individu,time_recov,j,posisi_x,posisi_y)
    sum_terinfeksi = infcount[j]
    totalday = j
    count_day[j] = j
    print('Hari ke',j,sum_terinfeksi,'orang')
    if(sum_terinfeksi == 0 and j > 0): #iterasi akan berhenti ketika jumlah terinfeksi sudah menemukan angka 0
        break
        
print('Total Hari Kasus',totalday)
#create figure animation
fig = plt.figure(num = 0, figsize = (15, 12))
create = dict()
ax01 = plt.subplot2grid((2, 2), (0, 0))
plt.xlabel('x')
plt.ylabel('y')
ax02 = plt.subplot2grid((2, 2), (0, 1))
plt.xlabel('days')
plt.ylabel('Number of infected people')

 
p12, = ax02.plot(count_day,infcount,'-b')

for i in range (sum_individu):
  create['p'+str(i+1)], = ax01.plot(posisi_x[i][0],posisi_y[i][0],'o',c='b')
  if (inf_people[i][0] > 0):
        create['p'+str(i+1)], = ax01.plot(posisi_x[i][0],posisi_y[i][0],'o',c='r')
  elif (inf_people[i][0] < 0 ):
        create['p'+str(i+1)], = ax01.plot(posisi_x[i][0],posisi_y[i][0],'o',c='b')
anim = animation.FuncAnimation(fig, animate,frames=400, interval=150, blit=False,repeat=True)
plt.show()