import matplotlib.dates as mdates
import matplotlib.pyplot as plt

from app.economics.wallet import Wallet


class Plotter:
    def __init__(self, config):
        self.config = config

    def print_agent_value_history(self, wallet: Wallet, generation, benchmark_wallet):
        x = mdates.date2num(wallet.valueTimestamps)
        y = wallet.valueHistory
        benchmark_wallet = benchmark_wallet[: len(x)]  # lol
        plt.xticks(rotation=45)
        plt.gcf().subplots_adjust(bottom=0.15)
        plt.plot_date(
            x,
            benchmark_wallet,
            color="#d62f2f",
            linestyle="solid",
            marker="",
            label="Target",
        )
        plt.plot_date(x, y, "-g", label="Total value")
        plt.legend(loc="upper left")
        plt.savefig(f"{self.config.path_to_config}/{str(generation)}.png", dpi=500)
        plt.close()

    def print_best_agents_learning_performance(self, best_scores, learning_targets):
        plt.plot(best_scores, label="Best agent end value")
        plt.axhline(
            learning_targets, color="r", linestyle="--", label="Target end value"
        )
        plt.legend(loc="upper left")
        plt.savefig(f"{self.config.path_to_config}/elite_perf_learning.png", dpi=500)
        plt.close()

    def print_best_agents_testing_performance(self, best_scores, testing_targets):
        for idx in range(len(self.config.validations)):
            plt.plot(best_scores[idx], label="Best agent end value")
            plt.axhline(
                testing_targets[idx],
                color="r",
                linestyle="--",
                label="Target end value",
            )
            plt.legend(loc="upper left")
            plt.savefig(
                f"{self.config.path_to_config}/elite_perf_test_{str(idx)}.png", dpi=500
            )
            plt.close()
