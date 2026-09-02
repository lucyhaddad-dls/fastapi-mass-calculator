from sample_mass_calcs.formulas import formula_from_ratios

def formula_from_mass_ratios(formula_list:list[str],
                             ratios:list[float|int],
                             keep_order:bool=True)->str:
    for i in range(len(ratios)):
        if isinstance(ratios[i], str):
            ratios[i] = float(ratios[i])

    formula_out = formula_from_ratios(formulae=formula_list,
                                      ratios=ratios,
                                      keep_order=keep_order)
    return formula_out