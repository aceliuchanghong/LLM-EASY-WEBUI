class chatMsg:
    def __init__(
            self,
            sim_model: str = "auto",
            gen_model: str = "auto",
    ):
        self.gen_model = gen_model
        self.sim_model = sim_model
        print(self.sim_model + self.gen_model)

    def __str__(self):
        return f"Similarity model: {self.sim_model}, Generate model: {self.gen_model}"
