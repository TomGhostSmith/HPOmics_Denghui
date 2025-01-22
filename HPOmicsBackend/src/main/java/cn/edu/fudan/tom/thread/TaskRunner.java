package cn.edu.fudan.tom.thread;

import cn.edu.fudan.tom.config.Config;
import cn.edu.fudan.tom.utils.TaskUtils;

import java.io.BufferedReader;
import java.io.File;
import java.io.InputStream;
import java.io.InputStreamReader;

public class TaskRunner extends Thread
{
    @Override
    public void run()
    {
        super.run();
        String nextTask;
        while ((nextTask = TaskUtils.getNextTaskName()) != null)
        {
            System.out.println("run task " + nextTask);
            runTask(nextTask);
        }
    }

    private void runTask(String taskName)
    {
        String[] command = {Config.PYTHON_PATH, Config.PYSCRIPT_PATH, taskName};
        ProcessBuilder pb = new ProcessBuilder(command);
        pb.directory(new File(Config.PROTOTYPE_PATH));
        pb.redirectErrorStream(true);
        pb.environment().put("PYTHONDONTWRITEBYTECODE", "1");
        try
        {
            Process process = pb.start();
            InputStream inputStream = process.getInputStream();
            BufferedReader bufferedReader = new BufferedReader(new InputStreamReader(inputStream));

            String line;
            while ((line = bufferedReader.readLine()) != null)
            {
                System.out.println(line);
                System.out.flush();
            }
            process.waitFor();

            System.out.println("Exit value: " + process.exitValue());
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

    }
}
