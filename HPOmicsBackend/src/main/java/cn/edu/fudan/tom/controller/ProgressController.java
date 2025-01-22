package cn.edu.fudan.tom.controller;

import cn.edu.fudan.tom.entity.Result;
import cn.edu.fudan.tom.entity.Task;
import cn.edu.fudan.tom.entity.TaskCase;
import cn.edu.fudan.tom.utils.TaskUtils;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
public class ProgressController
{
    @CrossOrigin
    @GetMapping("/getAllProgress")
    public ResponseEntity<List<Task>> getAllProgress()
    {
        return new ResponseEntity<>(TaskUtils.getTaskList(), HttpStatus.OK);
    }

    @CrossOrigin
    @GetMapping("/getTaskProgress/{taskName}")
    public ResponseEntity<List<TaskCase>> getTaskProgress(@PathVariable("taskName") String taskName)
    {
        return new ResponseEntity<>(TaskUtils.getTaskCaseList(taskName), HttpStatus.OK);
    }

    @CrossOrigin
    @GetMapping("/getResult/{taskName}/{patientIdentity}")
    public ResponseEntity<List<Result>> getResult(@PathVariable("taskName")String taskName, @PathVariable("patientIdentity")String patientIdentity)
    {
        return new ResponseEntity<>(TaskUtils.getResult(taskName, patientIdentity), HttpStatus.OK);
    }
}
