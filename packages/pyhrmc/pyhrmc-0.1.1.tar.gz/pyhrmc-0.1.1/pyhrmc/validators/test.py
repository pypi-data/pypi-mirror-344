        AvgCoordination = None        
self.avg_coordination = AvgCoordination

def avg_cn(self, struct):
        avg_cn = {}
        el_list = struct.el_list
        total_num_atoms = len(struct.sites)
        num_atoms = {}
        i = 0
        for el in el_list:
            avg_cn[el] = 0
            if idx > 0:
                num_atoms[el] = switch_list[idx] - switch_list[switch_idx - 1]
            i += 1
        num_atoms[el_list[-1]] = total_num_atoms - switch_list[i]

        switch_idx = 0
        switch_list = struct.el_switch
        for idx, site in enumerate(struct.sites):
            if idx < switch_list[switch_idx]:
                pass
            else:
                switch_idx += 1   
            avg_cn[el_list[switch_idx]] += site.cn[el_nn]

        for key in avg_cn:
            avg_cn[key] = avg_cn[key] / num_atoms[key]


        chi2 = 0
        for avg, target in zip(avg_cn, target_avg_cn):
            chi2 += (avg - target)**2 / coord_constant**2 
        
        return chi2