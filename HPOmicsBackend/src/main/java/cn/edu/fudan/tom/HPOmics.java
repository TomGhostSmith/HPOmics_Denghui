package cn.edu.fudan.tom;

import cn.edu.fudan.tom.config.Config;
import cn.edu.fudan.tom.config.StatusManager;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.File;

@SpringBootApplication
public class HPOmics
{
    public static void main(String[] args)
    {
        new File(Config.PATIENT_PATH).mkdirs();
        new File(Config.VCF_PATH).mkdirs();
        new File(Config.TASK_PATH).mkdirs();
        SpringApplication.run(HPOmics.class, args);
        StatusManager.startProcess();
    }
}
