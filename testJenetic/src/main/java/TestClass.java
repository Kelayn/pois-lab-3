import io.jenetics.DoubleChromosome;
import io.jenetics.DoubleGene;
import io.jenetics.Genotype;
import io.jenetics.Phenotype;
import io.jenetics.engine.Engine;
import io.jenetics.engine.EvolutionResult;
import io.jenetics.util.Factory;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

import java.util.List;
import java.util.stream.Collectors;

public class TestClass {

    public static final Logger logger =  LoggerFactory.getLogger(TestClass.class);

    public static final int POPULATION = 40;

    public static Factory<Genotype<DoubleGene>> genotypeFactory() {
        DoubleGene gene = DoubleGene.of(-2d, 10d);
        DoubleChromosome chromosome = DoubleChromosome.of(gene);
        return Genotype.of(chromosome);
    }

    public static Double eval(Genotype<DoubleGene> genotype) {
        double value = genotype.chromosome().gene().doubleValue();
        return (value - 4) * (value - 1) * (value + 2);
    }



    public static void main(String[] args) {
        Engine<DoubleGene, Double> engine = Engine.builder(TestClass::eval, genotypeFactory())
                .minimizing().populationSize(POPULATION).build();
//        Phenotype<DoubleGene, Double> phenotype =
//                engine.stream()
//                        .limit(100)
//                        .collect(EvolutionResult.toBestPhenotype());
//                System.out.println("Found " + phenotype.genotype().gene().doubleValue() + " = " + phenotype.fitness());
        List<EvolutionResult<DoubleGene, Double>> results = engine.stream()
                .limit(POPULATION)
                .collect(Collectors.toList()); results.forEach(result -> {
            Double value = result.bestPhenotype().genotype().gene().doubleValue();
            Double fitness = result.bestPhenotype().fitness();
            long generation = result.generation();
            logger.info("Generation #{}. Best genotype is {}, its value is {}", generation, value, fitness);
        });
    }
}
