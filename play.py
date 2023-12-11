import multiprocessing
import game


def play_game(board, comp_count, lock, iters):
    for _ in range(iters):
        game.create(board)
        while not game.isFinished(board):
            if game.isHumTurn(board):
                # game.inputRandom(board)
                game.inputHeuristic(board)
            else:
                game.inputMC(board)
        if game.value(board) == 10**20:
            with lock:
                comp_count.value += 1


if __name__ == "__main__":
    board = game.game()
    game.create(board)

    game.decideWhoIsFirst(board)

    comp_count = multiprocessing.Value("i", 0)
    lock = multiprocessing.Lock()

    iters = 25
    threads = 4
    processes = [
        multiprocessing.Process(target=play_game, args=(board, comp_count, lock, iters))
        for _ in range(threads)
    ]
    [process.start() for process in processes]
    [process.join() for process in processes]

    print(f"The MC agent beat the baseline: {comp_count.value} out of {iters * threads}")
