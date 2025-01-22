package cn.edu.fudan.tom.entity;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

import java.util.List;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class Result
{
    String diseaseID;
    String diseaseName;
    String[] overlapHPO;
    String[] excessHPO;
    String[] lossHPO;
    String possibility;
}
