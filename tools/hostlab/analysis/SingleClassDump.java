import jadx.api.JadxArgs;
import jadx.api.JadxDecompiler;
import jadx.api.JavaClass;

import java.nio.file.Path;
import java.util.Set;

/** Minimal single-class decompiler with resource and Java-input scanning disabled. */
public final class SingleClassDump {
    public static void main(String[] args) throws Exception {
        if (args.length < 2 || args.length > 3) {
            throw new IllegalArgumentException(
                "usage: SingleClassDump <apk> <raw-class-name> [method-short-id]"
            );
        }
        JadxArgs jadxArgs = new JadxArgs();
        var codeOutput = System.out;
        System.setOut(System.err);
        jadxArgs.setOutDir(Path.of(System.getProperty("hostlab.output")).toFile());
        jadxArgs.setInputFile(Path.of(args[0]).toAbsolutePath().normalize().toFile());
        jadxArgs.setSkipResources(true);
        jadxArgs.setDeobfuscationOn(false);
        jadxArgs.setThreadsCount(1);
        jadxArgs.setUseImports(false);
        jadxArgs.setDebugInfo(false);
        jadxArgs.setDisabledPlugins(Set.of("java-input"));
        jadxArgs.getDisabledPasses().add("UsageInfoVisitor");
        try (JadxDecompiler decompiler = new JadxDecompiler(jadxArgs)) {
            decompiler.load();
            JavaClass target = decompiler.getClassesWithInners().stream()
                .filter(candidate -> args[1].equals(candidate.getRawName()))
                .findFirst()
                .orElse(null);
            if (target == null) throw new ClassNotFoundException(args[1]);
            if (args.length == 3) {
                target.decompile();
                var method = target.searchMethodByShortId(args[2]);
                if (method == null) throw new NoSuchMethodException(args[2]);
                codeOutput.print(method.getCodeStr());
            } else {
                codeOutput.print(target.getCode());
            }
        }
    }
}
