package cn.edu.fudan.tom.controller;

import cn.edu.fudan.tom.config.Config;
import cn.edu.fudan.tom.dto.MultiplePatientTaskDTO;
import cn.edu.fudan.tom.dto.SinglePatientTaskDTO;
import cn.edu.fudan.tom.utils.TaskUtils;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.File;

@RestController
public class PatientController
{
    @CrossOrigin
    @PostMapping("/uploadPatient")
    public ResponseEntity uploadPatient(@RequestParam("file")MultipartFile uploadFile)
    {
        try
        {
            File file = new File(Config.PATIENT_PATH + "/" + uploadFile.getOriginalFilename());
            uploadFile.transferTo(file);
            return new ResponseEntity(HttpStatus.OK);
        }
        catch (Exception e)
        {
            e.printStackTrace();
            return new ResponseEntity(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }


    @CrossOrigin
    @PostMapping("/uploadVCF")
    public ResponseEntity uploadVCF(@RequestParam("file")MultipartFile uploadFile)
    {
        try
        {
            File file = new File(Config.VCF_PATH + "/" + uploadFile.getOriginalFilename());
            uploadFile.transferTo(file);
            return new ResponseEntity(HttpStatus.OK);
        }
        catch (Exception e)
        {
            e.printStackTrace();
            return new ResponseEntity(HttpStatus.INTERNAL_SERVER_ERROR);
        }
    }

    @CrossOrigin
    @PostMapping("/addSinglePatientTask")
    public ResponseEntity addSinglePatientTask(@RequestBody SinglePatientTaskDTO taskDTO)
    {
        Long taskName = taskDTO.createTask();
        System.out.println("Create task " + taskName);
        TaskUtils.tryStartProcess();
        return new ResponseEntity(HttpStatus.OK);
    }

    @CrossOrigin
    @PostMapping("/addMultiplePatientTask")
    public ResponseEntity addMultiplePatientTask(@RequestBody MultiplePatientTaskDTO taskDTO)
    {
        Long taskName = taskDTO.createTask();
        System.out.println("Create task " + taskName);
        TaskUtils.tryStartProcess();
        return new ResponseEntity(HttpStatus.OK);
    }
}

