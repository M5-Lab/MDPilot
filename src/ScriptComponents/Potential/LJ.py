import Potential

class LJ(Potential):

    def __init__(self, epsilon : float, sigma : float, r_cut : float, shift : bool = True):
        self.epsilon = epsilon
        self.sigma = sigma
        self.r_cut = r_cut
        self.shift = shift


    def generate_script_text(self):
        pair_style = f"pair_style lj/cut {self.r_cut}\n"
        pair_coeff = f"pair_coeff 1 1 {self.epsilon} {self.sigma}\n"
        shift_str = ""
        if self.shift:
            shift_str = f"pair_modify shift yes \n"
        return  pair_style + pair_coeff + shift_str