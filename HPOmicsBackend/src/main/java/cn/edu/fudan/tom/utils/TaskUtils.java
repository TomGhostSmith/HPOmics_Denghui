package cn.edu.fudan.tom.utils;

import cn.edu.fudan.tom.config.Config;
import cn.edu.fudan.tom.config.StatusManager;
import cn.edu.fudan.tom.entity.Result;
import cn.edu.fudan.tom.entity.Setting;
import cn.edu.fudan.tom.entity.Task;
import cn.edu.fudan.tom.entity.TaskCase;
import com.alibaba.fastjson.JSONWriter;

import java.io.*;
import java.nio.charset.StandardCharsets;
import java.text.SimpleDateFormat;
import java.util.*;

public class TaskUtils
{
    private static SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss");

    public static void writeSettings(Setting setting, Long taskName)
    {
        String filePath = Config.TASK_PATH + "/" + taskName + "/settings.json";

        try
        {
            Writer writer = new FileWriter(filePath, StandardCharsets.UTF_8);
            JSONWriter jsonWriter = new JSONWriter(writer);
            jsonWriter.writeObject(setting);
            jsonWriter.flush();
            jsonWriter.close();
            writer.close();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
    }

    public static List<Task> getTaskList()
    {
        File[] taskFolders = new File(Config.TASK_PATH).listFiles();
        Arrays.sort(taskFolders, new Comparator<File>() {
            @Override
            public int compare(File file1, File file2) {
                long timestamp1 = Long.parseLong(file1.getName());
                long timestamp2 = Long.parseLong(file2.getName());
                return Long.compare(timestamp2, timestamp1);
            }
        });
        List<Task> tasks = new ArrayList<>();
        for (File taskFolder : taskFolders)
        {
            String taskName = taskFolder.getName();
            String submitTime = getTaskName(Long.parseLong(taskName));
            File patientFolder = new File(Config.TASK_PATH + "/" + taskName + "/patient");
            File splitResultFolder = new File(Config.TASK_PATH + "/" + taskName + "/splitResult");
            File finalResultFolder = new File(Config.TASK_PATH + "/" + taskName + "/finalResult");
            int fileCount = patientFolder.listFiles() == null? 0 : patientFolder.listFiles().length;
            int splitResultCount = splitResultFolder.listFiles() == null? 0 : splitResultFolder.listFiles().length;
            int finalResultCount = finalResultFolder.listFiles() == null? 0 : finalResultFolder.listFiles().length;
            double progress = ((double)splitResultCount + finalResultCount) / fileCount * 50;
            tasks.add(new Task(taskName, submitTime, fileCount, String.format("%.2f", progress)));
        }
        return tasks;
    }

    public static List<TaskCase> getTaskCaseList(String taskName)
    {
        List<TaskCase> res;
        File[] patients = new File(Config.TASK_PATH + "/" + taskName + "/patient").listFiles();
        File[] splitResults = new File(Config.TASK_PATH + "/" + taskName + "/splitResult").listFiles();
        File[] finalResults = new File(Config.TASK_PATH + "/" + taskName + "/finalResult").listFiles();
        int patientCount = patients == null? 0 : patients.length;
        int splitResultCount = splitResults == null? 0 : splitResults.length;
        int finalResultCount = finalResults == null? 0 : finalResults.length;
        if (patientCount == finalResultCount)   // all done
        {
            List<TaskCase> taskCases = new ArrayList<>();
            for (File patient : patients)
            {
                String fileName = patient.getName();
                String patientIdentity = fileName.substring(0, fileName.length() - 5);
                taskCases.add(new TaskCase(patientIdentity, 2));
            }
            res = taskCases;
        }
        else if (patientCount == splitResultCount)   // Phen2Disease done
        {
            Map<String, TaskCase> taskCaseMap = new HashMap<>();
            for (File patient : patients)
            {
                String fileName = patient.getName();
                String patientIdentity = fileName.substring(0, fileName.length() - 5);
                taskCaseMap.put(patientIdentity, new TaskCase(patientIdentity, 1));
            }
            if (finalResultCount > 0)
            {
                for (File finalResult : finalResults)
                {
                    String fileName = finalResult.getName();
                    String patientIdentity = fileName.substring(0, fileName.length() - 4);
                    taskCaseMap.get(patientIdentity).addStatus();
                }
            }
            res = new ArrayList<>(taskCaseMap.values());
        }
        else  // still in Phen2Disease
        {
            Map<String, TaskCase> taskCaseMap = new HashMap<>();
            for (File patient : patients)
            {
                String fileName = patient.getName();
                String patientIdentity = fileName.substring(0, fileName.length() - 5);
                taskCaseMap.put(patientIdentity, new TaskCase(patientIdentity, 0));
            }
            if (splitResultCount > 0)
            {
                for (File splitResult : splitResults)
                {
                    String fileName = splitResult.getName();
                    String patientIdentity = fileName.substring(0, fileName.length() - 4);
                    taskCaseMap.get(patientIdentity).addStatus();
                }
            }
            res = new ArrayList<>(taskCaseMap.values());
        }
        Collections.sort(res, new Comparator<TaskCase>()
        {
            @Override
            public int compare(TaskCase o1, TaskCase o2)
            {
                int r = Integer.compare(o2.getStatus(), o1.getStatus());
                if (r == 0)
                {
                    r = o1.getPatientIdentity().compareTo(o2.getPatientIdentity());
                }
                return r;
            }
        });
        return res;
    }

    public static List<Result> getResult(String taskName, String patientIdentity)
    {
        List<Result> results = new ArrayList<>();
        String fileName = Config.TASK_PATH + "/" + taskName + "/finalResult/" + patientIdentity + ".csv";
        try
        {
            BufferedReader reader = new BufferedReader(new FileReader(fileName));
            String line;
            reader.readLine();   // skip the title line
            while ((line = reader.readLine()) != null)
            {
                if (line.endsWith(","))
                {
                    line += " ";
                }
                String[] terms = line.split(",");
                String diseaseID = terms[0];
                String diseaseName = terms[1];
                String possibility = String.format("%.2f", Double.parseDouble(terms[2]) * 100);
                String[] overlapHPO = terms[3].split(";");
                String[] excessHPO = terms[4].split(";");
                String[] lossHPO = terms[5].split(";");
                results.add(new Result(diseaseID, diseaseName, overlapHPO, excessHPO, lossHPO, possibility));
            }
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }
        return results;
    }

    public static String getNextTaskName()
    {
        String nextTask = null;
        File[] tasks = new File(Config.TASK_PATH).listFiles();
        Arrays.sort(tasks, new Comparator<File>() {
            @Override
            public int compare(File file1, File file2) {
                long timestamp1 = Long.parseLong(file1.getName());
                long timestamp2 = Long.parseLong(file2.getName());
                return Long.compare(timestamp1, timestamp2);
            }
        });
        for (File task : tasks)
        {
            File finalResultFolder = new File(Config.TASK_PATH + "/" + task.getName() + "/finalResult");
            int finalResultCount = finalResultFolder.listFiles() == null? 0 : finalResultFolder.listFiles().length;
            File patientFolder = new File(Config.TASK_PATH + "/" + task.getName() + "/patient");
            int patientFileCount = patientFolder.listFiles() == null? 0 : patientFolder.listFiles().length;
            if (finalResultCount != patientFileCount)
            {
                nextTask = task.getName();
                break;
            }
        }
        return nextTask;
    }

    public static void tryStartProcess()
    {
        if (!StatusManager.isRunning())
        {
            StatusManager.startProcess();
        }
    }

    public static String getTaskName(Long taskName)
    {
        return dateFormat.format(new Date(taskName));
    }
}
