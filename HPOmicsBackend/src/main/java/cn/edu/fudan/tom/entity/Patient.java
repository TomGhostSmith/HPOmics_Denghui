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
public class Patient
{
    String identity;
    Integer gender;
    Integer age;  // day. Month=30*day. Year = 365*day
    List<String> hpoList;
    String vcfFileName;
}
