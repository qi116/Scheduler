import java.util.ArrayList;
import java.util.Comparator;
import java.util.Random;
public class OverlapFinder {

    public ArrayList<double[]> availableTime (ArrayList<double[]> schedules){

        ArrayList<double[]> res = new ArrayList<>();

        // Initialize min_time to current time
        double curr_time = schedules.get(0)[0];

        // Loop through all intervals
        for(double[] interval : schedules){
            double st_tm = interval[0];
            double end_tm = interval[1];

            if(curr_time < st_tm){  //if current time is < start time of the interval
                //if(st_tm - curr_time >= min_duration){  //if the time between the 2 is greater than min_duration
                double[] t = {curr_time, st_tm}   ;
                res.add(t);
                curr_time = end_tm; // Update end time to be current_time
            } else {
                curr_time = Math.max(end_tm, curr_time); // For overlapping intervals, make sure you tax the max between current time and end time
            }
        }
        return res;

    }

    public static int randInt(int min, int max){
        Random r = new Random();
        return r.nextInt((max - min) + 1) + min;
    }

    public static void main(String[] args){
        ArrayList<double[]> schedules = new ArrayList<>();
        Random r = new Random();
        for (int i = 0; i < Math.pow(10,6);i++){
            //ArrayList<double[]> person = new ArrayList<double[]>();
            for (int j = 0; j < 5;j++){
                int offset = randInt(2,(int)Math.pow(10,6));
                double[] temp = { r.nextDouble()*2 + offset,r.nextDouble()*3 + offset + 3};
                schedules.add(temp);
            }
        }
        // Sort array by start time
        schedules.sort(Comparator.comparingDouble(a -> a[0]));

        OverlapFinder overlapFinder = new OverlapFinder();
        final long startTime = System.currentTimeMillis();
        System.out.println(overlapFinder.availableTime(schedules));
        final long endTime = System.currentTimeMillis();
        System.out.println("Total execution time: " + (endTime - startTime));
    }
}
