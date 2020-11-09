def pytest_addoption(parser):
    parser.addoption("--all", action="store_true", help="run all combinations")


def pytest_generate_tests(metafunc):
    if "positions" in metafunc.fixturenames:
        if metafunc.config.getoption("all"):
            end = 32
        else:
            end = 0
        metafunc.parametrize("positions", [([i,j],[k,l]) for i in range(end)
                                           for j in range(end)
                                           for k in range(end)
                                           for l in range(end) if (i,j) != (k,l)])