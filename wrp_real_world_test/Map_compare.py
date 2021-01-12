import numpy as np
import pickle as pickle
from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from Maps_data import MAP_A as map_b_real
#from Maps_data import res_map as map_b_result

class map_deffrent:
     """
     the main class
     """
     def __init__(self, real_map, file_name):
         self.real_map = real_map
         #self.result_map
         self.start = " upper_Right"
         self.location = np.array([0.2, 0.2])
         self.detla = 0.05
         self.delta_real = 0.2
         self.wall_limit = 65
         self.seen_limit =90
         self.move_ratio = int(self.delta_real/self.detla)
         self.seen = np.zeros((1, 2))
         self.mees = np.zeros((1, 2))
         self.whacres = self.get_whacers(file_name)

     # self.get_start()


     def show(self, a, fig_num=1, show=False, seen=False):
         ax = plt.figure(fig_num)
         ax = plt.imshow(a)
         if seen:
             b=np.argwhere(a==0)
             ax = plt.scatter(b[:,1],b[:,0], 10, color='blue')

         if show:
             plt.show()
         return ax

     def get_start(self):

        world_start = int(np.round(0.5 / self.detla))
        world_end = int(np.round(4.9 / self.detla))
        #result_map = result_map[world_start:world_end, world_start:world_end]

     def check_border(self, x, y):
        x=int(x)
        y=int(y)
        if  self.real_map[x+1, y] == 1 or self.real_map[x-1, y] ==1 or self.real_map[x, y+1] ==1 or self.real_map[x, y-1] ==1 :
            return True
        else:
            return False

     def if_seen(self,temp_arr, y, x):
        white = (np.sum(temp_arr > -1) / self.move_ratio ** 2) * 100

        if(self.check_border(x,y)):
            if(not white > self.wall_limit):
                x=1
            return white>self.wall_limit
        else:
            return white>self.seen_limit

     def get_whacers(self, file_name):
         w = dict()
         geeky_file = open(file_name, 'rt')
         lines = geeky_file.read().split('\n')
         for l in lines:
             if l != '':
                 dictionary = dict()
                 # Removes curly braces and splits the pairs into a list
                 pairs = l.strip('{}').split(', ')
                 for i in pairs:
                     pair = i.split(': ')
                     tmpstr = np.array(
                         [pair[1][1:-1].replace('[', "").replace(']', "").replace('}', "").split(',')]).astype(np.int)

                     tmpstr = tmpstr.reshape(int(len(tmpstr[0]) / 2), 2).tolist()

                     dictionary[pair[0][1:-1]] = tmpstr
                 w.update(dictionary)
         geeky_file.close()
         return w

     def comapre_point(self, cell,result_map):

         start_x=int((cell[0]-1)*self.move_ratio)
         end_x=start_x+self.move_ratio
         start_y=int((cell[1]-1)*self.move_ratio)
         end_y=start_y+self.move_ratio
         temp_arr =result_map[start_y: end_y, start_x: end_x]
         if not self.if_seen(temp_arr, cell[0], cell[1]):
             print(cell)
             print('x-> ',start_x,' : ', end_x)
             print('y-> ',start_y,' : ', end_y)

         return self.if_seen(temp_arr,cell[0] ,cell[1])


     def compare_map(self,no_map, resolt_map,whach,path):

        self.show(no_map, 6, show=False)
        gray = self.define_non_obsticle()


        for cell in whach:
            if(cell.tolist() not in self.seen.tolist()):
                if self.comapre_point(cell, resolt_map):
                    self.seen = np.append(self.seen, [cell], axis=0)
                else:
                    self.mees = np.append(self.mees, [cell], axis=0)

      #  for index, cell in enumerate(self.mees[1:].tolist()):
      #      if cell in self.seen.tolist():
      #          self.mees=np.delete(self.mees,index+1,axis=0)

        '''
        for i in range(1, 22):
            for j in range(1, 22):
        #for cell in np.int32(no_map):
                cell=[i,j]
                if self.comapre_point(cell,resolt_map):
                    green= np.append(g, [cell], axis=0)
                else:
                    red = np.append(r, [cell], axis=0)
        '''
        print(len(self.seen))
        plt.scatter(gray[:, 1], gray[:, 0], 40, color='gray')
        plt.scatter(self.seen[1:, 0], self.seen[1:, 1], 40, color='green')
        plt.scatter(self.mees[1:, 0], self.mees[1:, 1], 40, color='orange')
        a = self.get_problom_unseen(path)
        return a

     def get_seen_cells(self, cell):
         return np.array(self.whacres[str(round(cell[1] / 0.2)) + ',' + str(round(cell[0] / 0.2))])

     def get_problom_unseen(self,path):
         need_to_see=np.zeros((1,2))
         for  cell in self.mees[1:].tolist():
             tmp=True
             for step in path:
                 t = self.get_seen_cells(step).tolist()
                 if(cell in t):
                     tmp=False
                     break
             if(tmp):
                need_to_see=np.append(need_to_see,[cell],axis=0)

         plt.scatter(need_to_see[1:, 0], need_to_see[1:, 1], 40, color='red')

         return need_to_see[1:]

     def define_obsticle(self):
        obsicals_arr = np.argwhere(self.real_map == 1)
        return np.float64(obsicals_arr)

     def define_non_obsticle(self):
        obsicals_arr = np.argwhere(self.real_map == 0)
        return np.float64(obsicals_arr)





if __name__ == '__main__':
    map_deffrent = map_deffrent(map_b_real)
    map_deffrent.define_obsticle()
    map_deffrent.show(map_deffrent.result_map, 2, False, True)
    map_deffrent.show(map_deffrent.real_map, 1, False, True)
    r=map_deffrent.compare_map()
    print(r)
    plt.show()

