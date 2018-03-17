package org.sphere.diploma;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.conf.Configured;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.lib.input.KeyValueTextInputFormat;
import org.apache.hadoop.mapreduce.lib.input.MultipleInputs;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.Tool;
import org.apache.hadoop.util.ToolRunner;

import java.io.IOException;

public class MRPhotobankFilterJob extends Configured implements Tool {

    public int run(String[] args) throws Exception {
        Job job = getJobConf(this.getConf(), args[0], args[1]);
        return (job.waitForCompletion(true)? 0: 1);
    }

    private static Job getJobConf(Configuration conf, String input_pattern, String output_dir) throws IOException {
        Job job = Job.getInstance(conf);

        job.setJarByClass(MRPhotobankFilterJob.class);
        job.setJobName(MRPhotobankFilterJob.class.getCanonicalName());

        // Using MultipleInputs class to apply input patterns. Setting input format.
        MultipleInputs.addInputPath(job, new Path(input_pattern), KeyValueTextInputFormat.class);
        // Set output dir to create
        FileOutputFormat.setOutputPath(job, new Path(output_dir));

        // Set output format
        job.setOutputFormatClass(TextOutputFormat.class);

        // Set output types
        job.setMapOutputKeyClass(null);
        job.setMapOutputValueClass(null);
        job.setOutputKeyClass(null);
        job.setOutputValueClass(null);

        // Set MR classes
        //job.setMapperClass(MRPhotobankFilterMapper.class);
        //job.setPartitionerClass(MRPhotobankFilterPartitioner.class);
        //job.setReducerClass(MRPhotobankFilterReducer.class);

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
