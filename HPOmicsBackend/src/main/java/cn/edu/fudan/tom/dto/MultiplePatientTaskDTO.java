package cn.edu.fudan.tom.dto;

import cn.edu.fudan.tom.config.Config;
import cn.edu.fudan.tom.entity.Setting;
import cn.edu.fudan.tom.utils.TaskUtils;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.io.*;
import java.nio.file.Files;
import java.nio.file.Paths;
import java.util.List;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class MultiplePatientTaskDTO
{
    List<String> patientFileNames;
    List<String> vcfFileNames;
    Setting setting;

    public Long createTask()
    {
        Long taskName = System.currentTimeMillis();

        String folderPath = Config.TASK_PATH +  "/" + taskName;
        String patientPath = folderPath + "/patient";
        String VCFPath = folderPath + "/VCF";
        String CADDPath = folderPath + "/CADD";
        String splitResultPath = folderPath + "/splitResult";
        String finalResultPath = folderPath + "/finalResult";
        new File(patientPath).mkdirs();
        new File(VCFPath).mkdirs();
        new File(CADDPath).mkdirs();
        new File(splitResultPath).mkdirs();
        new File(finalResultPath).mkdirs();


        TaskUtils.writeSettings(setting, taskName);


        for (String VCFFileName : vcfFileNames)
        {
            try
            {
                Files.move(
                        Paths.get(Config.VCF_PATH + "/" + VCFFileName),
                        Paths.get(VCFPath + "/" + VCFFileName)
                );
            }
            catch (Exception e)
            {
                e.printStackTrace();
            }
        }

        for (String patientFileName : patientFileNames)
        {
            try
            {
                Files.move(
                        Paths.get(Config.PATIENT_PATH + "/" + patientFileName),
                        Paths.get(patientPath + "/" + patientFileName)
                );
            }
            catch (Exception e)
            {
                e.printStackTrace();
            }
        }

        return taskName;
    }
}
