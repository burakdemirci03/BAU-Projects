import java.util.concurrent.Semaphore;

public class Main {
    public static void main(String[] args) {
        ReadWriteLock RWLock = new ReadWriteLock();

        Thread reader1 = new Thread(() -> {
            RWLock.readLock();
            System.out.println("Reader 1 is reading.");
            try{
                Thread.sleep(4000);
            }
            catch(InterruptedException e){}
            System.out.println("Reader 1 finished reading.");
            RWLock.readUnlock();
        });

        Thread reader2 = new Thread(() -> {
            RWLock.readLock();
            System.out.println("Reader 2 is reading.");
            try{
                Thread.sleep(2000);
            }
            catch(InterruptedException e){}
            System.out.println("Reader 2 finished reading.");
            RWLock.readUnlock();
        });

        Thread reader3 = new Thread(() -> {
            RWLock.readLock();
            System.out.println("Reader 3 is reading.");
            try{
                Thread.sleep(500);
            }
            catch(InterruptedException e){}
            System.out.println("Reader 3 finished reading.");
            RWLock.readUnlock();
        });

        Thread reader4 = new Thread(() -> {
            RWLock.readLock();
            System.out.println("Reader 4 is reading.");
            try{
                Thread.sleep(1000);
            }
            catch(InterruptedException e){}
            System.out.println("Reader 4 finished reading.");
            RWLock.readUnlock();
        });

        Thread writer1 = new Thread(() -> {
            RWLock.writeLock();
            System.out.println("Writer 1 is writing.");
            try{
                Thread.sleep(2000);
            }
            catch(InterruptedException e){}
            System.out.println("Writer 1 finished writing.");
            RWLock.writeUnlock();
        });

        Thread writer2 = new Thread(() -> {
            RWLock.writeLock();
            System.out.println("Writer 2 is writing.");
            try{
                Thread.sleep(3000);
            }
            catch(InterruptedException e){}
            System.out.println("Writer 2 finished writing.");
            RWLock.writeUnlock();
        });

        Thread writer3 = new Thread(() -> {
            RWLock.writeLock();
            System.out.println("Writer 3 is writing.");
            try{
                Thread.sleep(2500);
            }
            catch(InterruptedException e){}
            System.out.println("Writer 3 finished writing.");
            RWLock.writeUnlock();
        });

        writer1.start();
        reader1.start();
        writer2.start();
        reader2.start();
        reader3.start();
        reader4.start();
        writer3.start();
    }
}


class ReadWriteLock {
    private Semaphore r_mut = new Semaphore(1);
    private Semaphore S = new Semaphore(1);
    private int read_num = 0;

    public void readLock() {
        try {
            System.out.println("\033[0;31m" + "# A reader is trying to read." + "\033[0m");
            r_mut.acquire();
            } catch (Exception e) {}
            read_num++;
            if (read_num == 1) {
                try {
                    S.acquire();
                } catch (Exception e) {}
            }
            r_mut.release();
    }

    public void readUnlock() {
        read_num--;
        if (read_num == 0) {
            S.release();
        }
    }

    public void writeLock() {
        try {
            System.out.println("\033[0;31m" + "# A writer is trying to write." + "\033[0m");
            S.acquire();
        } catch (Exception e) {}
    }

    public void writeUnlock() {
        S.release(); 
    }
}
