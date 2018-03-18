package org.sphere.diploma;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.BytesWritable;
import org.apache.hadoop.io.NullWritable;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import java.io.IOException;

/**
 * Filtering job class. Filters pb2 packed images, outputs pb2 packed images.
 */
public class MRPhotobankFilterJob extends Configured implements Tool {

    public int run(String args[]) throws Exception {
        Job job = getJobConf(this.getConf(), args[0], args[1]);
        return (job.waitForCompletion(true)? 0: 1);
    }

    private static Job getJobConf(Configuration conf, String input_pattern, String output_dir) throws IOException {
        Job job = Job.getInstance(conf);

        // Set jar and job name
        job.setJarByClass(MRPhotobankFilterJob.class);
        job.setJobName(MRPhotobankFilterJob.class.getCanonicalName());

        // Using MultipleInputs class to apply input patterns. Setting input format.
        MultipleInputs.addInputPath(job, new Path(input_pattern), StorageInputFormat.class);
        // Set output dir to create
        FileOutputFormat.setOutputPath(job, new Path(output_dir));

        // Set output format
        job.setOutputFormatClass(StorageOutputFormat.class);

        // Set output types
        job.setMapOutputKeyClass(NullWritable.class);
        job.setMapOutputValueClass(BytesWritable.class);
        job.setOutputKeyClass(NullWritable.class);
        job.setOutputValueClass(BytesWritable.class);

        // Set MR classes
        job.setMapperClass(MRPhotobankFilterMapper.class);
        job.setPartitionerClass(MRPhotobankFilterPartitioner.class);
        job.setReducerClass(MRPhotobankFilterReducer.class);

        return job;
    }

    public static void main(String[] args) throws Exception {
        // Check for input and output
        if (args.length < 2) {
            System.err.println("ERROR: Need at least two arguments: <input_pattern> <output_dir>.");
            System.exit(1);
        }

        // Run job
        int return_code = ToolRunner.run(MRPhotobankFilterJob.class.newInstance(), args);
        System.exit(return_code);
    }
}
