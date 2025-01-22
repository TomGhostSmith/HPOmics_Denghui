package cn.edu.fudan.tom.entity;

import lombok.AllArgsConstructor;
import lombok.Getter;
import lombok.NoArgsConstructor;
import lombok.Setter;

@Getter
@Setter
@AllArgsConstructor
@NoArgsConstructor
public class Setting
{
    Integer taskType;
    Integer icMethod;
    Integer similarity;
    Integer useAncestor;
    Integer convertProportionMethod;
    Double convertMaxProportion;
    Boolean usePPI;
    Double ppiSelfProportion;
    Double ppiDirectProportion;
    Double ppiIndirectProportion;
    Integer caddMethod;
    Double caddMaxProportion;
}
