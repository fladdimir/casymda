import sys

sys.path.append(".")

import examples.wait_for_interrupt.test_wait_for_interrupt_visual as test

if __name__ == "__main__":
    test.FLOW_SPEED = 200
    test.test_visualized_run()
