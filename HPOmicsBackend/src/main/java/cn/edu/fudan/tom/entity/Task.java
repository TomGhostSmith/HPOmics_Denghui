package cn.edu.fudan.tom.entity;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class Task
{
    String taskName;
    String submitTime;
    Integer taskCount;
    String progress;
}
