package cn.edu.fudan.tom.dto;

import cn.edu.fudan.tom.config.Config;
import cn.edu.fudan.tom.entity.Patient;
import cn.edu.fudan.tom.entity.Setting;
import cn.edu.fudan.tom.utils.TaskUtils;
import com.alibaba.fastjson.JSONWriter;
import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.io.File;
import java.io.FileWriter;
import java.io.Writer;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Paths;

@Getter
@Setter
@NoArgsConstructor
@AllArgsConstructor
public class SinglePatientTaskDTO
{
    Patient patient;
    Setting setting;

    public Long createTask()
    {
//        List<Patient> patientList = new ArrayList<>();
//        patientList.add(patient);
//        Task task = new Task(patientList, setting);

        Long taskName = System.currentTimeMillis();

        String folderPath = Config.TASK_PATH +  "/" + taskName;
        String patientPath = folderPath + "/patient";
        String VCFPath = folderPath + "/VCF";
        String CADDPath = folderPath + "/CADD";
        String splitResultPath = folderPath + "/splitResult";
        String finalResultPath = folderPath + "/finalResult";
        String patientFilePath = patientPath + "/" + patient.getIdentity() + ".json";
        new File(patientPath).mkdirs();
        new File(VCFPath).mkdirs();
        new File(CADDPath).mkdirs();
        new File(splitResultPath).mkdirs();
        new File(finalResultPath).mkdirs();

        try
        {
            Writer writer = new FileWriter(patientFilePath, StandardCharsets.UTF_8);
            JSONWriter jsonWriter = new JSONWriter(writer);
            jsonWriter.writeObject(patient);
            jsonWriter.flush();
            jsonWriter.close();
            writer.close();
        }
        catch (Exception e)
        {
            e.printStackTrace();
        }

        TaskUtils.writeSettings(setting, taskName);

        String VCFFileName = patient.getVcfFileName();

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



        return taskName;
    }
}
