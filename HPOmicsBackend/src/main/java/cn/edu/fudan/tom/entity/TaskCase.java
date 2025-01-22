package cn.edu.fudan.tom.entity;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class TaskCase
{
    String patientIdentity;
    Integer status;

    public void addStatus()
    {
        this.status ++;
    }
}
