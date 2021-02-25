from time import strftime, localtime


class GeneticAlgorithmWorkerJson:
    def __init__(self, agents, targets, config):
        self.timestamp = strftime("%Y-%m-%d %H-%M-%S", localtime())
        self.fitness_start = config.start_date
        self.fitness_end = config.end_date

        self.validations = []
        for idx, target in enumerate(targets):
            self.validations.append(
                {
                    "start_date": config.validations[idx][0],
                    "end_date": config.validations[idx][1],
                    "target": target,
                }
            )
        self.start_cash = config.start_cash
        self.agents = list(map(lambda ag: ag.to_json_ready(), agents))
