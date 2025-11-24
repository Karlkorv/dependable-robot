public class Assignment2 {
    static class WorldState {
        static volatile boolean waitingPositionAvailable = true;
        static volatile boolean loadingPositionAvailable = true;
        static volatile boolean boxInFetchingPosition = false;
        static volatile boolean boxOnBack = false;
    }

    static class CB {
        double signalRate = 0.6;
        double softwareFailureRate = 0.08;

        boolean signalRobotToMoveToLoadingPosition() {
            printProgress("CB: Attempting to signal robot to move to loading position ", 3, 300);
            if (Math.random() < softwareFailureRate) {
                System.out.println(red("CB: software glitch, not sending correct signal"));
                return false;
            }
            boolean s = Math.random() < signalRate;
            System.out.println("CB: signal sent? " + s);
            return s;
        }

        boolean signalGrabBox() {
            printProgress("CB: Attempting to signal robot to grab box ", 3, 300);
            boolean s = Math.random() < signalRate;
            System.out.println("CB: grab signal sent? " + s);
            return s;
        }

        boolean signalRobotAtLoadingPosition() {
            printProgress("CB: Attempting to acknowledge robot at loading position ", 3, 300);
            boolean s = Math.random() < signalRate;
            System.out.println("CB: ack signal sent? " + s);
            return s;
        }

        boolean signalRobotToDeliverBox() {
            printProgress("CB: Attempting to signal robot to deliver box ", 3, 300);
            boolean s = Math.random() < signalRate;
            System.out.println("CB: deliver signal sent? " + s);
            return s;
        }

        boolean deliverBoxToFetchingPosition() {
            printProgress("CB: Attempting to move box to belt ", 3, 300);
            boolean s = Math.random() < 0.9;
            System.out.println("CB: box moved to belt? " + s);
            return s;
        }
    }

    static class Robot {
        boolean inWaitingPosition = false;
        boolean inLoadingPosition = false;
        boolean grippingBox = false;
        double softwareFailureRate = 0.05;

        void sleepMs(long ms) {
            try {
                Thread.sleep(ms);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }

        void printDots(int count, long betweenMs) {
            for (int i = 0; i < count; i++) {
                System.out.print(".");
                System.out.flush();
                sleepMs(betweenMs);
            }
            System.out.println();
        }

        void printProgress(String message, int dots, long betweenMs) {
            System.out.print(message);
            printDots(dots, betweenMs);
        }

        String red(String s) {
            return "\u001B[31m" + s + "\u001B[0m";
        }

        boolean inWaitingPosition() {
            return inWaitingPosition;
        }

        boolean inLoadingPosition() {
            return inLoadingPosition;
        }

        void moveToWaitingPosition() {
            printProgress("Robot: Moving to waiting position ", 4, 300);
            sleepMs(600);
            inWaitingPosition = true;
            inLoadingPosition = false;
            System.out.println("Robot: inWaitingPosition=" + inWaitingPosition);
        }

        void moveToLoadingPosition() {
            printProgress("Robot: Moving to loading position ", 4, 300);
            sleepMs(600);
            inWaitingPosition = false;
            inLoadingPosition = true;
            System.out.println("Robot: inLoadingPosition=" + inLoadingPosition);
        }

        boolean awaitSignalInWaitingPosition(boolean incomingSignal) {
            printProgress("Robot: Awaiting signal in waiting position ", 3, 300);
            sleepMs(400);
            boolean received = incomingSignal && Math.random() < 0.9;
            System.out.println("Robot: signal received? " + received);
            if (received) {
                boolean available = radarCheckWaiting();
                System.out.println("Robot: waiting position available? " + available);
                return available;
            }
            return false;
        }

        boolean awaitSignalToMoveToLoadingPosition(boolean incomingSignal) {
            printProgress("Robot: Awaiting move-to-loading signal ", 3, 300);
            sleepMs(400);
            boolean received = incomingSignal && Math.random() < 0.9;
            System.out.println("Robot: move signal received? " + received);
            if (received) {
                boolean available = radarCheckLoading();
                System.out.println("Robot: loading position available? " + available);
                return available;
            }
            return false;
        }

        boolean awaitSignalGrabBox(boolean incomingSignal) {
            printProgress("Robot: Awaiting grab-box signal from CB ", 3, 300);
            sleepMs(400);
            boolean received = incomingSignal && Math.random() < 0.9;
            System.out.println("Robot: grab signal received? " + received);
            return received;
        }

        boolean radarCheckWaiting() {
            printProgress("Robot: Checking waiting position with radar ", 3, 100);
            sleepMs(400);
            if (Math.random() < softwareFailureRate) {
                System.out.println(red("Robot: radar false negative/positive"));
                return !WorldState.waitingPositionAvailable;
            }
            return WorldState.waitingPositionAvailable;
        }

        boolean radarCheckLoading() {
            printProgress("Robot: Checking loading position with radar ", 3, 100);
            sleepMs(400);
            if (Math.random() < softwareFailureRate) {
                System.out.println(red("Robot: radar false reading"));
                return !WorldState.loadingPositionAvailable;
            }
            return WorldState.loadingPositionAvailable;
        }

        boolean weightCheckBack() {
            printProgress("Robot: Checking back weight sensor ", 3, 100);
            sleepMs(300);
            if (Math.random() < softwareFailureRate) {
                System.out.println(red("Robot: weight sensor unreliable"));
                return !WorldState.boxOnBack;
            }
            return WorldState.boxOnBack;
        }

        void signalCBLoadingEntered() {
            printProgress("Robot: Signalling CB that loading position entered ", 3, 300);
            sleepMs(200);
            WorldState.loadingPositionAvailable = false;
        }

        void signalCBOperationComplete() {
            printProgress("Robot: Signalling CB operation complete ", 3, 300);
            sleepMs(200);
            WorldState.loadingPositionAvailable = true;
        }

        void pickBoxFromFetching() {
            printProgress("Robot: Closing gripper to pick box ", 3, 300);
            sleepMs(400);
            grippingBox = true;
            WorldState.boxInFetchingPosition = false;
            WorldState.boxOnBack = true;
            System.out.println("Robot: grippingBox=" + grippingBox + " boxOnBack=" + WorldState.boxOnBack);
        }
    }

    static void printDots(int count, long betweenMs) {
        for (int i = 0; i < count; i++) {
            System.out.print(".");
            System.out.flush();
            try {
                Thread.sleep(betweenMs);
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
            }
        }
        System.out.println();
    }

    static void printProgress(String message, int dots, long betweenMs) {
        System.out.print(message);
        printDots(dots, betweenMs);
    }

    static String red(String s) {
        return "\u001B[31m" + s + "\u001B[0m";
    }

    static String green(String s) {
        return "\u001B[32m" + s + "\u001B[0m";
    }

    public static void main(String[] args) {
        Robot robot = new Robot();
        CB cb = new CB();

        System.out.println();
        System.out.println("Starting simulation");
        System.out.println();

        robot.moveToWaitingPosition();

        boolean signal = false;
        int waitAttempts = 0;
        int maxWaitAttempts = 8;
        while (robot.inWaitingPosition() && waitAttempts < maxWaitAttempts) {
            boolean handled = robot.awaitSignalInWaitingPosition(signal);
            if (handled) {
                printProgress("Main: robot accepted signal and waiting position verified ", 3, 300);
                break;
            }
            signal = cb.signalRobotToMoveToLoadingPosition();
            waitAttempts++;
        }
        if (!robot.inWaitingPosition() || waitAttempts >= maxWaitAttempts) {
            System.out.println(red("Main: Timeout waiting for move-to-loading signal or position not available"));
            return;
        }

        boolean moveAllowed = robot.awaitSignalToMoveToLoadingPosition(signal);
        if (!moveAllowed) {
            System.out.println(red("Main: Move to loading denied after verification"));
            return;
        }

        robot.moveToLoadingPosition();
        robot.signalCBLoadingEntered();

        int deliverAttempts = 0;
        do {
            WorldState.boxInFetchingPosition = cb.deliverBoxToFetchingPosition();
            deliverAttempts++;
        } while (!WorldState.boxInFetchingPosition && deliverAttempts < 5);

        boolean grabSignal = false;
        int grabAttempts = 0;
        int maxGrabAttempts = 6;
        while (robot.inLoadingPosition() && grabAttempts < maxGrabAttempts) {
            boolean received = robot.awaitSignalGrabBox(grabSignal);
            if (received) {
                if (WorldState.boxInFetchingPosition) {
                    robot.pickBoxFromFetching();
                    boolean weightOk = robot.weightCheckBack();
                    System.out.println("Main: weight check says boxOnBack=" + weightOk);
                    if (!weightOk) {
                        System.out.println(red("Main: Weight sensor disagrees, aborting fetch"));
                        return;
                    }
                    robot.signalCBOperationComplete();
                    System.out.println(green("Main: Box has been fetched"));
                    break;
                } else {
                    System.out.println(red("Main: No box in fetching position"));
                    return;
                }
            }
            grabSignal = cb.signalGrabBox();
            grabAttempts++;
        }
        if (grabAttempts >= maxGrabAttempts) {
            System.out.println(red("Main: Timeout waiting for grab-box signal"));
            return;
        }

        System.out.println();
        System.out.println(green("Simulation finished"));
    }
}
