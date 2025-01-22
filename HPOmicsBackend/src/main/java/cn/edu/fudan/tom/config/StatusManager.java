package cn.edu.fudan.tom.config;

import cn.edu.fudan.tom.thread.TaskRunner;

public class StatusManager
{
    private static final StatusManager instance = new StatusManager();
    private StatusManager() {}
    private TaskRunner taskRunner = null;

    public static void startProcess()
    {
        if (instance.taskRunner == null || !instance.taskRunner.isAlive())
        {
            instance.taskRunner = new TaskRunner();
            instance.taskRunner.start();
        }
    }

    public static boolean isRunning()
    {
        return instance.taskRunner != null && instance.taskRunner.isAlive();
    }
}
