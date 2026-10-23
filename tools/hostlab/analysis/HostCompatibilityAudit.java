import jadx.api.JadxArgs;
import jadx.api.JadxDecompiler;
import jadx.api.plugins.input.insns.Opcode;
import jadx.core.dex.instructions.args.ArgType;
import jadx.core.dex.nodes.ClassNode;
import jadx.core.dex.nodes.FieldNode;
import jadx.core.dex.nodes.MethodNode;

import java.io.BufferedWriter;
import java.nio.charset.StandardCharsets;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.StandardCopyOption;
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.function.Predicate;

/**
 * Offline, read-only compatibility audit for host APKs.
 *
 * The checks intentionally mirror VersionAdapter's conservative structural rules. They do not
 * claim runtime/UI verification; their job is to expose candidate drift before device testing.
 */
public final class HostCompatibilityAudit {
    private static final String VIEW = "android.view.View";
    private static final String ACTIVITY = "android.app.Activity";
    private static final String LIST = "java.util.List";
    private static final String STRING = "java.lang.String";
    private static final String VOID = "void";
    private static final String INT = "int";

    private final Map<String, ClassNode> classes;
    private final Collection<ClassNode> allClasses;
    private final BufferedWriter writer;
    private final boolean exhaustiveQuality;

    private HostCompatibilityAudit(
        Map<String, ClassNode> classes,
        Collection<ClassNode> allClasses,
        BufferedWriter writer,
        boolean exhaustiveQuality
    ) {
        this.classes = classes;
        this.allClasses = allClasses;
        this.writer = writer;
        this.exhaustiveQuality = exhaustiveQuality;
    }

    public static void main(String[] args) throws Exception {
        if (args.length < 2 || args.length > 3) {
            throw new IllegalArgumentException(
                "usage: HostCompatibilityAudit <apk> <output-tsv> [quality-all]"
            );
        }
        Path apk = Path.of(args[0]).toAbsolutePath().normalize();
        Path output = Path.of(args[1]).toAbsolutePath().normalize();
        if (!Files.isRegularFile(apk)) {
            throw new IllegalArgumentException("invalid apk: " + apk);
        }

        JadxArgs jadxArgs = new JadxArgs();
        jadxArgs.setInputFile(apk.toFile());
        jadxArgs.setSkipResources(true);
        jadxArgs.setSkipSources(true);
        jadxArgs.setDeobfuscationOn(false);
        // Structural checks use raw DEX names; Java identifier aliases are unnecessary.
        // Deobfuscation=false alone still runs the global RenameVisitor in JADX 1.5.6.
        jadxArgs.setRenameFlags(Set.of());
        jadxArgs.setThreadsCount(1);
        jadxArgs.setUseImports(false);
        jadxArgs.setDebugInfo(false);
        jadxArgs.setDisabledPlugins(Set.of("java-input"));
        jadxArgs.getDisabledPasses().add("UsageInfoVisitor");
        jadxArgs.getDisabledPasses().add("RenameVisitor");

        Files.createDirectories(output.getParent());
        try (JadxDecompiler decompiler = new JadxDecompiler(jadxArgs)) {
            decompiler.load();
            List<ClassNode> allClasses = decompiler.getRoot().getClasses(true);
            Map<String, ClassNode> classes = new HashMap<>(allClasses.size() * 2);
            for (ClassNode cls : allClasses) {
                classes.put(rawName(cls), cls);
            }
            Path partial = output.resolveSibling(output.getFileName() + ".partial");
            try (BufferedWriter writer = Files.newBufferedWriter(partial, StandardCharsets.UTF_8)) {
                HostCompatibilityAudit audit = new HostCompatibilityAudit(
                    classes,
                    allClasses,
                    writer,
                    args.length == 3 && "quality-all".equals(args[2])
                );
                audit.write("META", "apk", apk.getFileName().toString());
                audit.write("META", "class_count", Integer.toString(allClasses.size()));
                audit.run();
                audit.write("META", "audit_complete", "true");
            }
            Files.move(partial, output, StandardCopyOption.REPLACE_EXISTING,
                StandardCopyOption.ATOMIC_MOVE);
        }
    }

    private void run() throws Exception {
        List<String> blockCandidates = List.of(
            "ar1.c",
            "gr1.c",
            "mq1.c",
            "Ip1.c", "Ro1.c", "Sn1.c", "Wm1.c", "wm1.c", "dl1.c",
            "Uj1.c", "Ch1.c", "kh1.c", "ih1.c",
            "Xg1.c", "Lg1.c", "Kg1.c", "od1.c", "Sb1.c",
            "xb1.c", "Pa1.c", "si6.c", "oe6.c", "vd6.c",
            "id6.c", "wc6.c", "xc6.c", "aa6.c", "o56.c"
        );
        List<String> qualityCandidates = List.of(
            "Rs1.j",
            "Xs1.j",
            "es1.i",
            "Ar1.l", "Jq1.l", "Kp1.l", "Oo1.i", "oo1.g", "Vm1.i",
            "Kl1.j", "tj1.g", "bj1.i", "Zi1.h",
            "Oi1.f", "Ci1.f", "Bi1.f", "Ze1.h", "Dd1.h",
            "hd1.h", "zc1.h", "dm6.h", "zh6.h", "gh6.h",
            "tg6.h", "hg6.h",
            "com.bilibili.playerbizcommon.utils.PlayerSettingHelper"
        );

        List<MethodRef> blockMatches = discoverMethods(method ->
            !isStatic(method) && !isAbstract(method) &&
                "tv.danmaku.bili.update.model.BiliUpgradeInfo".equals(typeName(method.getReturnType())) &&
                args(method).equals(List.of("android.content.Context"))
        );
        feature(
            "block_update",
            knownOwnerMatches(blockMatches, blockCandidates) ? "FOUND" : "MISSING",
            refs(blockMatches)
        );
        discovery("block_update", blockMatches);

        List<MethodRef> semanticQualityMatches = discoverQualityMethods(qualityCandidates);
        List<MethodRef> structuralQualityMatches = methodsOf(qualityCandidates, method ->
            !isAbstract(method) && args(method).isEmpty() && INT.equals(typeName(method.getReturnType())) &&
                Set.of("a", "c", "getDefaultQuality")
                    .contains(method.getMethodInfo().getName())
        );
        boolean qualityVerified = semanticQualityMatches.stream()
            .anyMatch(structuralQualityMatches::contains);
        feature(
            "player_default_quality",
            qualityVerified ? "FOUND" : (structuralQualityMatches.isEmpty() ? "MISSING" : "PARTIAL"),
            "semantic=" + refs(semanticQualityMatches) + ";structural=" + refs(structuralQualityMatches)
        );
        discovery("player_default_quality", semanticQualityMatches);

        auditCommentCopy();
        auditDescriptionCopy();
        auditHomeTopBar();
        auditMine();
        auditDynamicTabs();
        auditFullNumber();
        auditPlayerUi();
        auditHomeRecommend();
        auditVideoRelate();
        auditHomeTabs();
        auditMineComponents();
        auditStory();
        auditSplash();
        auditBottomBar();
        auditTeenagersMode();
        auditCommentData();
        auditCommentTopology();
        auditCommentSection();
        auditPausedAd();
        auditBanner();
        auditDirectFeatures();
    }

    private void auditCommentCopy() throws Exception {
        List<String> lowOwners = List.of(
            "com.bilibili.app.comment3.ui.holder.t0",
            "com.bilibili.app.comment3.ui.holder.h0"
        );
        List<MethodRef> low = methodsOf(lowOwners, method ->
            Set.of("o0", "q0").contains(method.getMethodInfo().getName())
        );

        List<String> highOwners = List.of(
            "com.bilibili.app.comment3.ui.nextholderexp3.handle.CommentNextExperiment3ContentRichTextHandler",
            "com.bilibili.app.comment3.ui.holder.handle.CommentContentRichTextHandler"
        );
        List<MethodRef> high = new ArrayList<>();
        for (String ownerName : highOwners) {
            ClassNode owner = classes.get(ownerName);
            if (owner == null || owner.getFields().stream().noneMatch(field ->
                typeName(field.getType()).endsWith(".CommentItem"))) {
                continue;
            }
            for (MethodNode method : owner.getMethods()) {
                if (isStatic(method) || method.getArgTypes().size() < 1 || method.getArgTypes().size() > 5) {
                    continue;
                }
                boolean hasBinding = method.getArgTypes().stream()
                    .map(this::classOf)
                    .filter(java.util.Objects::nonNull)
                    .anyMatch(parameter -> parameter.getFields().stream().anyMatch(field ->
                        isSubclassOf(raw(field.getType()), VIEW)));
                if (hasBinding) {
                    high.add(new MethodRef(ownerName, method.getMethodInfo().getShortId()));
                }
            }
        }
        feature(
            "comment_free_copy",
            high.isEmpty() && low.isEmpty() ? "MISSING" : (high.isEmpty() ? "PARTIAL" : "FOUND"),
            "high=" + refs(high) + ";low=" + refs(low)
        );
    }

    private void auditDescriptionCopy() throws Exception {
        boolean expandable = classes.containsKey(
            "tv.danmaku.bili.videopage.common.widget.view.ExpandableTextView"
        ) || classes.containsKey(
            "com.mall.videodetail.vd.videopage.common.widget.view.ExpandableTextView"
        );
        List<MethodRef> officialCopy = methodsOf(List.of(
            "com.bilibili.ship.theseus.ugc.intro.ugcheadline.UgcHeadlineService$b",
            "com.bilibili.ship.theseus.ugc.intro.ugcheadline.UgcHeadlineService$c"
        ), method -> {
            String name = method.getMethodInfo().getName();
            List<String> args = args(method);
            return ("c".equals(name) && args.equals(List.of(STRING, "boolean"))) ||
                (("w".equals(name) || "o".equals(name)) &&
                    args.equals(List.of("boolean", STRING)));
        });
        feature(
            "description_free_copy",
            expandable && !officialCopy.isEmpty() ? "FOUND" : "MISSING",
            "expandable=" + expandable + ";official=" + refs(officialCopy)
        );
    }

    private void auditHomeTopBar() throws Exception {
        String menuOwner = "com.bilibili.lib.homepage.startdust.menu.a";
        List<MethodRef> game = methodsOf(List.of(menuOwner), method ->
            !isStatic(method) && VOID.equals(typeName(method.getReturnType())) &&
                args(method).equals(List.of("android.view.Menu", "android.view.MenuInflater"))
        );
        List<String> baseOwners = List.of(
            "tv.danmaku.bili.ui.main2.basic.BaseMainFrameFragment",
            "tv.danmaku.p9138bili.p9228ui.main2.basic.BaseMainFrameFragment"
        );
        List<MethodRef> base = methodsOf(baseOwners, method ->
            "onViewCreated".equals(method.getMethodInfo().getName()) && !isStatic(method) &&
                VOID.equals(typeName(method.getReturnType())) &&
                args(method).equals(List.of(VIEW, "android.os.Bundle"))
        );
        boolean switchField = baseOwners.stream().map(classes::get).filter(java.util.Objects::nonNull)
            .flatMap(owner -> owner.getFields().stream())
            .anyMatch(field -> typeName(field.getType()).endsWith(".SwitchTextView"));
        List<MethodRef> words = methodsOf(List.of(
            "tv.danmaku.bili.ui.main2.MainFragment",
            "tv.danmaku.p9138bili.p9228ui.main2.MainFragment"
        ), method -> !isStatic(method) && !isAbstract(method) &&
            VOID.equals(typeName(method.getReturnType())) && method.getArgTypes().size() == 1 &&
            Set.of("com.bilibili.app.comm.list.common.api.b", "com.bilibili.app.comm.list.common.api.d")
                .contains(typeName(method.getArgTypes().get(0)))
        );
        feature(
            "home_top_bar",
            !base.isEmpty() && switchField && (!game.isEmpty() || !words.isEmpty()) ? "FOUND" :
                (!game.isEmpty() || !words.isEmpty() || !base.isEmpty() ? "PARTIAL" : "MISSING"),
            "game=" + refs(game) + ";base=" + refs(base) + ";switch=" + switchField +
                ";words=" + refs(words)
        );
    }

    private void auditMine() throws Exception {
        String fragmentName = "tv.danmaku.bili.ui.main2.mine.HomeUserCenterFragment";
        ClassNode fragment = classes.get(fragmentName);
        List<MethodRef> builds = methodsOf(List.of(fragmentName), method ->
            isStatic(method) && VOID.equals(typeName(method.getReturnType())) &&
                args(method).equals(List.of(fragmentName, "tv.danmaku.bili.ui.main2.api.AccountMine"))
        );
        long listFields = fragment == null ? 0 : fragment.getFields().stream()
            .filter(field -> !isStatic(field) && isSubclassOf(raw(field.getType()), LIST)).count();
        boolean click = methodsOf(List.of(fragmentName + "$e", fragmentName + "$i"), method ->
            !isStatic(method) && VOID.equals(typeName(method.getReturnType())) &&
                args(method).equals(List.of("com.bilibili.lib.homepage.mine.MenuGroup$Item"))
        ).size() == 1;
        feature(
            "mine_entry",
            !builds.isEmpty() && listFields == 1 && click ? "FOUND" : "MISSING",
            "build=" + refs(builds) + ";listFields=" + listFields + ";click=" + click
        );

        String managerName = "tv.danmaku.bili.ui.main2.mine.modularvip.MineVipModuleManager";
        ClassNode manager = classes.get(managerName);
        long managerFields = fragment == null ? 0 : fragment.getFields().stream()
            .filter(field -> !isStatic(field) && isSubclassOf(raw(field.getType()), managerName)).count();
        List<FieldNode> bindings = manager == null ? List.of() : manager.getFields().stream()
            .filter(field -> !isStatic(field) && implementsInterface(typeName(field.getType()),
                "androidx.viewbinding.ViewBinding"))
            .toList();
        boolean root = bindings.size() == 1 && methodsIncludingSupers(typeName(bindings.get(0).getType())).stream()
            .anyMatch(method -> "getRoot".equals(method.getMethodInfo().getName()) &&
                !isStatic(method) && method.getArgTypes().isEmpty() &&
                isSubclassOf(raw(method.getReturnType()), VIEW));
        boolean resume = methodsOf(List.of(fragmentName), method ->
            "onResume".equals(method.getMethodInfo().getName()) && !isStatic(method) &&
                method.getArgTypes().isEmpty() && VOID.equals(typeName(method.getReturnType()))
        ).size() == 1;
        feature(
            "mine_vip",
            managerFields == 1 && bindings.size() == 1 && root && resume ? "FOUND" : "MISSING",
            "managerFields=" + managerFields + ";bindings=" + bindings.size() +
                ";root=" + root + ";resume=" + resume
        );
    }

    private void auditDynamicTabs() throws Exception {
        String fragmentName = "com.bilibili.bplus.followinglist.home.mediator.MediatorFragment";
        String tabName = "com.bilibili.bplus.followinglist.home.mediator.MediatorTabLayout";
        List<MethodNode> getters = declaredMethods(fragmentName).stream().filter(method ->
            !isStatic(method) && method.getArgTypes().isEmpty() && LIST.equals(raw(method.getReturnType()))
        ).toList();
        boolean itemFields = false;
        String item = "";
        if (getters.size() == 1) {
            List<ArgType> generics = getters.get(0).getReturnType().getGenericTypes();
            if (generics != null && generics.size() == 1) {
                item = raw(generics.get(0));
                ClassNode itemClass = classes.get(item);
                itemFields = itemClass != null && itemClass.getFields().stream().anyMatch(field ->
                    "a".equals(field.getName()) && STRING.equals(typeName(field.getType()))) &&
                    itemClass.getFields().stream().anyMatch(field ->
                        "b".equals(field.getName()) && STRING.equals(typeName(field.getType())));
            }
        }
        boolean tab = isSubclassOf(tabName, "com.google.android.material.tabs.TabLayout");
        feature(
            "dynamic_tabs",
            getters.size() == 1 && itemFields && tab ? "FOUND" : "MISSING",
            "getters=" + getters.size() + ";item=" + item + ";fields=" + itemFields + ";tab=" + tab
        );
    }

    private void auditFullNumber() throws Exception {
        List<String> owners = List.of(
            "com.bilibili.base.util.NumberFormat",
            "com.bilibili.p4566base.p4568util.NumberFormat",
            "com.bilibili.n9.util.NumberFormat",
            "com.bilibili.lib.utils.NumberFormat",
            "kntr.base.localization.NumberFormat_androidKt"
        );
        Set<String> names = Set.of("format", "formatWithComma", "formatNumber", "format$default", "formatNumber$default");
        List<MethodRef> found = methodsOf(owners, method -> {
            String first = method.getArgTypes().isEmpty() ? "" : typeName(method.getArgTypes().get(0));
            boolean acceptedFirst = Set.of("int", "long", "java.lang.Integer", "java.lang.Long").contains(first) ||
                (STRING.equals(first) && rawName(method.getParentClass()).equals("kntr.base.localization.NumberFormat_androidKt"));
            return isStatic(method) && STRING.equals(typeName(method.getReturnType())) &&
                names.contains(method.getMethodInfo().getName()) && method.getArgTypes().size() >= 1 &&
                method.getArgTypes().size() <= 5 && acceptedFirst;
        });
        feature("full_number", found.isEmpty() ? "MISSING" : "FOUND", refs(found));
    }

    private void auditPlayerUi() throws Exception {
        String portraitOwner = "com.bilibili.app.gemini.player.widget.story.GeminiPlayerFullStoryWidget";
        List<MethodRef> portrait = methodsOf(List.of(portraitOwner), method ->
            "setVisibility".equals(method.getMethodInfo().getName()) &&
                args(method).equals(List.of(INT)) && VOID.equals(typeName(method.getReturnType()))
        );
        feature("player_portrait", isSubclassOf(portraitOwner, VIEW) && !portrait.isEmpty() ? "FOUND" : "MISSING", refs(portrait));

        String activity = "com.bilibili.ship.theseus.detail.UnitedBizDetailsActivity";
        List<MethodRef> create = methodsOf(List.of(activity), method ->
            "onCreate".equals(method.getMethodInfo().getName()) && !isStatic(method) &&
                args(method).equals(List.of("android.os.Bundle")) && VOID.equals(typeName(method.getReturnType()))
        );
        feature("player_status_bar", isSubclassOf(activity, ACTIVITY) && !create.isEmpty() ? "FOUND" : "MISSING", refs(create));
    }

    private void auditHomeRecommend() throws Exception {
        String holder = "com.bilibili.pegasus.PegasusHolderData";
        boolean holderType = methodsIncludingSupers(holder).stream().anyMatch(method ->
            "getHolderType".equals(method.getMethodInfo().getName()) && !isStatic(method) &&
                method.getArgTypes().isEmpty() && STRING.equals(typeName(method.getReturnType())));
        List<String> responses = List.of(
            "com.bilibili.pegasus.data.base.PegasusResponse",
            "com.bilibili.pegasus.p5730data.p5731base.PegasusResponse",
            "com.bilibili.pegasus.p5730data.request.PegasusResponseWrapper"
        );
        List<MethodRef> items = methodsIncludingOwners(responses, method ->
            "getItems".equals(method.getMethodInfo().getName()) && !isStatic(method) &&
                !isAbstract(method) && method.getArgTypes().isEmpty() &&
                isSubclassOf(raw(method.getReturnType()), LIST));
        List<String> bases = List.of(
            "com.bilibili.pegasus.data.base.BasePegasusData",
            "com.bilibili.pegasus.p5730data.p5731base.BasePegasusData",
            holder
        );
        boolean uri = bases.stream().filter(classes::containsKey).findFirst()
            .map(base -> methodsIncludingSupers(base).stream().anyMatch(method ->
                "getUri".equals(method.getMethodInfo().getName()) && !isStatic(method) &&
                    method.getArgTypes().isEmpty() && STRING.equals(typeName(method.getReturnType()))))
            .orElse(false);
        feature("home_recommend", holderType && !items.isEmpty() && uri ? "FOUND" : "MISSING",
            "holder=" + holderType + ";items=" + refs(items) + ";uri=" + uri);
    }

    private void auditVideoRelate() throws Exception {
        List<MethodRef> lists = methodsIncludingOwners(List.of(
            "com.bapis.bilibili.app.viewunite.v1.Relates",
            "com.bapis.bilibili.app.viewunite.v1.RelatesFeedReply",
            "com.bapis.bilibili.app.view.v1.RelatesFeedReply",
            "com.bapis.bilibili.app.view.v1.ViewReply",
            "com.bapis.bilibili.app.view.v1.PlayerRelatesReply"
        ), method -> Set.of("getCardsList", "getRelatesList").contains(method.getMethodInfo().getName()) &&
            !isStatic(method) && !isAbstract(method) && method.getArgTypes().isEmpty() &&
            isSubclassOf(raw(method.getReturnType()), LIST));
        List<MethodRef> attributes = methodsIncludingOwners(List.of(
            "com.bapis.bilibili.app.viewunite.common.RelateCard",
            "com.bapis.bilibili.app.view.v1.Relate"
        ), method -> Set.of("getCardCase", "getGoto", "getCardType").contains(method.getMethodInfo().getName()) &&
            !isStatic(method) && method.getArgTypes().isEmpty() && !VOID.equals(typeName(method.getReturnType())));
        feature("video_relate", !lists.isEmpty() && !attributes.isEmpty() ? "FOUND" : "MISSING",
            "lists=" + refs(lists) + ";attributes=" + refs(attributes));
    }

    private void auditHomeTabs() throws Exception {
        List<String> owners = List.of(
            "tv.danmaku.bili.ui.main2.HomeFragmentV2",
            "tv.danmaku.p9138bili.p9228ui.main2.HomeFragmentV2"
        );
        List<MethodRef> matches = methodsOf(owners, method -> {
            if (isStatic(method) || isAbstract(method) || method.getArgTypes().size() != 1 ||
                !LIST.equals(raw(method.getArgTypes().get(0))) || !LIST.equals(raw(method.getReturnType()))) {
                return false;
            }
            return typeName(method.getArgTypes().get(0)).contains("main2.resource.");
        });
        feature("home_tabs", matches.size() == 1 ? "FOUND" : "MISSING", refs(matches));
    }

    private void auditMineComponents() throws Exception {
        List<String> groupOwners = List.of(
            "com.bilibili.lib.homepage.mine.MenuGroupV2",
            "com.bilibili.lib.homepage.mine.MenuGroup"
        );
        List<String> itemOwners = List.of(
            "com.bilibili.lib.homepage.mine.MenuGroupV2$Item",
            "com.bilibili.lib.homepage.mine.MenuGroup$Item"
        );
        List<MethodRef> lists = methodsIncludingOwners(groupOwners, method ->
            "getItemList".equals(method.getMethodInfo().getName()) &&
            !isStatic(method) && method.getArgTypes().isEmpty() &&
            isSubclassOf(raw(method.getReturnType()), LIST));
        List<MethodRef> titles = methodsIncludingOwners(itemOwners, method ->
            "getTitle".equals(method.getMethodInfo().getName()) && !isStatic(method) &&
            method.getArgTypes().isEmpty() && STRING.equals(typeName(method.getReturnType())));
        boolean legacyFields = false;
        for (String groupOwner : groupOwners) {
            ClassNode group = classes.get(groupOwner);
            if (group == null) continue;
            for (FieldNode field : group.getFields()) {
                if (isStatic(field) || field.getAccessFlags().isFinal() || !LIST.equals(raw(field.getType()))) {
                    continue;
                }
                List<ArgType> generics = field.getType().getGenericTypes();
                if (generics == null || generics.size() != 1) continue;
                String itemName = raw(generics.get(0));
                ClassNode item = itemOwners.contains(itemName) ? classes.get(itemName) : null;
                if (item != null && item.getFields().stream().anyMatch(candidate ->
                    !isStatic(candidate) && "title".equals(candidate.getName()) &&
                        STRING.equals(typeName(candidate.getType())))) {
                    legacyFields = true;
                }
            }
        }
        boolean getterPath = !lists.isEmpty() && !titles.isEmpty();
        feature("mine_components", getterPath || legacyFields ? "FOUND" : "MISSING",
            "lists=" + refs(lists) + ";titles=" + refs(titles) + ";legacy=" + legacyFields);
    }

    private void auditStory() throws Exception {
        String detail = "com.bilibili.video.story.StoryDetail";
        Set<String> booleanNames = Set.of("isAd", "isLive", "isGame", "isBangumi", "isCheese", "isMusic");
        List<MethodRef> semantics = methodsOf(List.of(detail), method ->
            booleanNames.contains(method.getMethodInfo().getName()) && !isStatic(method) &&
                method.getArgTypes().isEmpty() && "boolean".equals(typeName(method.getReturnType())));
        List<MethodRef> responses = methodsIncludingOwners(List.of("com.bilibili.video.story.api.StoryFeedResponse"), method ->
            "getItems".equals(method.getMethodInfo().getName()) && !isStatic(method) &&
                method.getArgTypes().isEmpty() && isSubclassOf(raw(method.getReturnType()), LIST));
        List<MethodRef> pager = methodsOf(List.of("com.bilibili.video.story.player.StoryPagerPlayer"), method ->
            !isStatic(method) && !isAbstract(method) && VOID.equals(typeName(method.getReturnType())) &&
                method.getArgTypes().size() == 1 && LIST.equals(raw(method.getArgTypes().get(0))) &&
                typeName(method.getArgTypes().get(0)).contains(detail));
        feature("story_purify", classes.containsKey(detail) && (!responses.isEmpty() || !pager.isEmpty()) &&
            !semantics.isEmpty() ? "FOUND" : "MISSING",
            "responses=" + refs(responses) + ";pager=" + refs(pager) + ";semantic=" + refs(semantics));
    }

    private void auditSplash() throws Exception {
        List<String> owners = List.of(
            "tv.danmaku.bili.splash.ad.model.SplashListResponse",
            "tv.danmaku.bili.splash.ad.model.SplashShowResponse",
            "tv.danmaku.bili.ui.splash.SplashData",
            "tv.danmaku.bili.ui.splash.ad.model.SplashData",
            "tv.danmaku.bili.ui.splash.ShowSplashData",
            "tv.danmaku.bili.ui.splash.ad.model.SplashShowData"
        );
        Set<String> names = Set.of("getSplashList", "getStrategyList", "getShowList", "getAdList");
        List<MethodRef> methods = methodsIncludingOwners(owners, method ->
            names.contains(method.getMethodInfo().getName()) && !isStatic(method) && !isAbstract(method) &&
                method.getArgTypes().isEmpty() && isSubclassOf(raw(method.getReturnType()), LIST));
        feature("splash_ads", methods.isEmpty() ? "MISSING" : "FOUND", refs(methods));
    }

    private void auditBottomBar() throws Exception {
        List<String> owners = List.of(
            "com.bilibili.lib.homepage.widget.TabHost",
            "com.bilibili.p5690lib.p5708homepage.widget.TabHost",
            "tv.danmaku.bili.ui.main2.widget.TabHost",
            "tv.danmaku.p9138bili.p9228ui.main2.widget.TabHost"
        );
        List<MethodRef> tabs = methodsIncludingOwners(owners, method ->
            "getTabs".equals(method.getMethodInfo().getName()) && !isStatic(method) &&
                method.getArgTypes().isEmpty() && isSubclassOf(raw(method.getReturnType()), LIST));
        List<MethodRef> binds = methodsOf(owners, method ->
            !isStatic(method) && VOID.equals(typeName(method.getReturnType())) &&
                method.getArgTypes().size() == 2 && INT.equals(typeName(method.getArgTypes().get(0))) &&
                isSubclassOf(raw(method.getArgTypes().get(1)), VIEW));
        feature("bottom_bar", tabs.size() == 1 && binds.size() == 1 ? "FOUND" : "MISSING",
            "tabs=" + refs(tabs) + ";binds=" + refs(binds));
    }

    private void auditTeenagersMode() throws Exception {
        List<MethodRef> create = methodsOf(List.of(
            "com.bilibili.teenagersmode.ui.TeenagersModeDialogActivity",
            "com.bilibili.app.preferences.TeenagersModeDialogActivity",
            "com.bilibili.p4439app.preferences.TeenagersModeDialogActivity",
            "tv.danmaku.bili.ui.teenagersmode.TeenagersModeDialogActivity"
        ), method -> "onCreate".equals(method.getMethodInfo().getName()) && !isStatic(method) &&
            args(method).equals(List.of("android.os.Bundle")) && VOID.equals(typeName(method.getReturnType())));
        feature("teenagers_mode", create.isEmpty() ? "MISSING" : "FOUND", refs(create));
    }

    private void auditCommentData() throws Exception {
        List<String> replyOwners = List.of(
            "com.bapis.bilibili.main.community.reply.v1.ReplyInfo",
            "com.bapis.bilibili.p4311main.community.reply.p4312v1.ReplyInfo"
        );
        String reply = replyOwners.stream().filter(classes::containsKey).findFirst().orElse("");
        boolean content = !reply.isEmpty() && hasNoArgMethod(reply, "getContent");
        boolean member = !reply.isEmpty() && hasNoArgMethod(reply, "getMember");
        List<MethodRef> lists = methodsIncludingOwners(List.of(
            "com.bapis.bilibili.main.community.reply.v1.MainListReply",
            "com.bapis.bilibili.p4311main.community.reply.p4312v1.MainListReply",
            reply
        ), method -> !isStatic(method) && method.getArgTypes().isEmpty() &&
            LIST.equals(raw(method.getReturnType())) && typeName(method.getReturnType()).contains(reply));
        feature("comment_filter", content && member && !lists.isEmpty() ? "FOUND" : "MISSING",
            "reply=" + reply + ";content=" + content + ";member=" + member + ";lists=" + refs(lists));

        List<MethodRef> urls = methodsIncludingOwners(List.of(
            "com.bapis.bilibili.main.community.reply.v1.Content",
            "com.bapis.bilibili.p4311main.community.reply.p4312v1.Content"
        ), method -> !isStatic(method) && method.getArgTypes().isEmpty() &&
            LIST.equals(raw(method.getReturnType())));
        boolean optionalPayloads = hasNoArgMethod(
            List.of(
                "com.bapis.bilibili.main.community.reply.v1.MainListReply",
                "com.bapis.bilibili.p4311main.community.reply.p4312v1.MainListReply"
            ),
            Set.of("hasQoe", "getQoe", "hasOperation", "getOperation", "hasOperationV2", "getOperationV2")
        );
        feature("comment_purify", !urls.isEmpty() || optionalPayloads ? "FOUND" : "MISSING",
            "listGetters=" + refs(urls) + ";optional=" + optionalPayloads);
    }

    /**
     * 回复脉络（comment_topology）。
     *
     * 之前该域完全不在审计范围内，导致 9.6.0 与 9.10.0 上 mapper facade 的混淆类名漂移
     * （c -> b）两次静默失效都没有被离线审计发现。这里刻意不按类名判断——facade 名在
     * b/c/d/e 之间来回跳——而是复刻运行期的结构规则：static + 非 abstract + 非 synthetic +
     * 返回 CommentItem + 首参 ReplyInfo，并额外记录命中的 owner 集合，便于换版后直接看出漂移。
     */
    private void auditCommentTopology() throws Exception {
        List<String> replyOwners = List.of(
            "com.bapis.bilibili.main.community.reply.v1.ReplyInfo",
            "com.bapis.bilibili.p4311main.community.reply.p4312v1.ReplyInfo"
        );
        String reply = replyOwners.stream().filter(classes::containsKey).findFirst().orElse("");
        String commentItem = "com.bilibili.app.comment3.data.model.CommentItem";
        if (reply.isEmpty() || !classes.containsKey(commentItem)) {
            feature("comment_topology", "MISSING",
                "reply=" + reply + ";commentItem=" + classes.containsKey(commentItem));
            return;
        }
        String replyPackage = reply.substring(0, reply.lastIndexOf('.'));

        List<MethodRef> mappers = discoverMethods(method ->
            isStatic(method) && !isAbstract(method) &&
                !method.getAccessFlags().isSynthetic() &&
                commentItem.equals(typeName(method.getReturnType())) &&
                !method.getArgTypes().isEmpty() &&
                reply.equals(typeName(method.getArgTypes().get(0)))
        );
        Set<String> mapperOwners = new LinkedHashSet<>(mappers.stream().map(MethodRef::owner).toList());

        Set<String> replyGetters = Set.of(
            "getId", "getOid", "getType", "getRoot", "getParent", "getDialog",
            "getCtime", "getCount", "getMid", "getContent", "getMemberV2", "getRepliesList"
        );
        List<String> missingReplyGetters = replyGetters.stream()
            .filter(name -> !hasNoArgMethod(reply, name))
            .sorted()
            .toList();

        boolean itemId = hasNoArgMethod(commentItem, "getId");
        boolean message = hasNoArgMethod(replyPackage + ".Content", "getMessage");
        boolean basicName = hasNoArgMethod(replyPackage + ".MemberV2$Basic", "getName");
        boolean nextOffset = hasNoArgMethod("com.bapis.bilibili.pagination.FeedPaginationReply", "getNextOffset");
        boolean detailRoot = hasNoArgMethod(replyPackage + ".DetailListReply", "getRoot")
            && hasNoArgMethod(replyPackage + ".DetailListReply", "getPaginationReply");

        String paginationBuilder = staticNoArgReturnType("com.bapis.bilibili.pagination.FeedPagination", "newBuilder");
        boolean pagination = !paginationBuilder.isEmpty()
            && !methodsOf(List.of(paginationBuilder), method ->
                !isStatic(method) && "setOffset".equals(method.getMethodInfo().getName()) &&
                    args(method).equals(List.of(STRING))).isEmpty()
            && hasNoArgMethod(paginationBuilder, "build");

        String detailBuilder = staticNoArgReturnType(replyPackage + ".DetailListReq", "newBuilder");
        Set<String> detailSetters = Set.of(
            "setOid", "setType", "setModeValue", "setPagination", "setRoot", "setRpid"
        );
        List<String> missingDetailSetters = detailBuilder.isEmpty()
            ? detailSetters.stream().sorted().toList()
            : detailSetters.stream()
                .filter(name -> methodsOf(List.of(detailBuilder), method ->
                    !isStatic(method) && name.equals(method.getMethodInfo().getName()) &&
                        method.getArgTypes().size() == 1).isEmpty())
                .sorted()
                .toList();
        boolean detail = !detailBuilder.isEmpty() && missingDetailSetters.isEmpty()
            && hasNoArgMethod(detailBuilder, "build");

        boolean moss = !methodsOf(List.of(replyPackage + ".ReplyMoss"), method ->
            !isStatic(method) && "detailList".equals(method.getMethodInfo().getName()) &&
                method.getArgTypes().size() == 2 &&
                (replyPackage + ".DetailListReq").equals(typeName(method.getArgTypes().get(0))) &&
                VOID.equals(typeName(method.getReturnType()))).isEmpty();

        boolean protocolOk = missingReplyGetters.isEmpty() && itemId && message && basicName
            && nextOffset && detailRoot && pagination && detail && moss;
        feature(
            "comment_topology",
            !mappers.isEmpty() && protocolOk ? "FOUND" : "MISSING",
            "mapperOwners=" + String.join(",", mapperOwners) +
                ";mappers=" + refs(mappers) +
                ";missingReplyGetters=" + String.join(",", missingReplyGetters) +
                ";itemId=" + itemId + ";message=" + message + ";basicName=" + basicName +
                ";pagination=" + pagination + ";detail=" + detail +
                ";missingDetailSetters=" + String.join(",", missingDetailSetters) +
                ";moss=" + moss + ";detailReply=" + detailRoot + ";nextOffset=" + nextOffset
        );
        discovery("comment_topology", mappers);
    }

    /** 返回 owner 上公开静态无参方法的返回类型名；缺失时返回空串。 */
    private String staticNoArgReturnType(String owner, String name) {
        return declaredMethods(owner).stream()
            .filter(method -> isStatic(method) && name.equals(method.getMethodInfo().getName()) &&
                method.getArgTypes().isEmpty())
            .map(method -> typeName(method.getReturnType()))
            .findFirst()
            .orElse("");
    }

    private void auditCommentSection() throws Exception {
        List<String> services = List.of(
            "com.bilibili.ship.theseus.united.page.tab.TheseusTabPagerService",
            "com.bilibili.p5797ship.theseus.united.p5850page.p5861tab.TheseusTabPagerService"
        );
        LinkedHashSet<MethodRef> constructors = new LinkedHashSet<>();
        LinkedHashSet<MethodRef> tagGetters = new LinkedHashSet<>();
        for (String serviceName : services) {
            ClassNode service = classes.get(serviceName);
            if (service == null) continue;
            LinkedHashSet<String> owners = new LinkedHashSet<>();
            owners.add(serviceName);
            for (MethodNode constructor : service.getMethods()) {
                if (!"<init>".equals(constructor.getMethodInfo().getName())) continue;
                constructor.getArgTypes().stream().map(HostCompatibilityAudit::raw)
                    .filter(classes::containsKey).forEach(owners::add);
            }
            for (String ownerName : owners) {
                ClassNode owner = classes.get(ownerName);
                if (owner == null) continue;
                for (MethodNode constructor : owner.getMethods()) {
                    if (!"<init>".equals(constructor.getMethodInfo().getName()) ||
                        constructor.getAccessFlags().isSynthetic()) {
                        continue;
                    }
                    for (int index = 0; index < constructor.getArgTypes().size(); index++) {
                        ArgType argument = constructor.getArgTypes().get(index);
                        if (!LIST.equals(raw(argument))) continue;
                        LinkedHashSet<String> itemNames = new LinkedHashSet<>();
                        addSingleGeneric(itemNames, argument);
                        for (FieldNode field : owner.getFields()) {
                            if (LIST.equals(raw(field.getType()))) {
                                addSingleGeneric(itemNames, field.getType());
                            }
                        }
                        for (String itemName : itemNames) {
                            ClassNode item = classes.get(itemName);
                            if (item == null) continue;
                            for (MethodNode getter : methodsIncludingSupers(itemName)) {
                                if (isStatic(getter) || !getter.getArgTypes().isEmpty()) continue;
                                String enumName = raw(getter.getReturnType());
                                ClassNode enumClass = classes.get(enumName);
                                if (enumClass == null || !enumClass.getAccessFlags().isEnum()) continue;
                                boolean hasComment = enumClass.getFields().stream().anyMatch(field ->
                                    isStatic(field) && field.getName().equalsIgnoreCase("Comment"));
                                if (!hasComment) continue;
                                constructors.add(new MethodRef(
                                    ownerName,
                                    constructor.getMethodInfo().getShortId() + "@" + index
                                ));
                                tagGetters.add(new MethodRef(
                                    rawName(getter.getParentClass()),
                                    getter.getMethodInfo().getShortId()
                                ));
                            }
                        }
                    }
                }
            }
        }
        feature(
            "comment_section",
            !constructors.isEmpty() && tagGetters.size() == 1 ? "FOUND" : "MISSING",
            "constructors=" + refs(new ArrayList<>(constructors)) +
                ";tags=" + refs(new ArrayList<>(tagGetters))
        );
    }

    private static void addSingleGeneric(Set<String> names, ArgType type) {
        List<ArgType> generics = type.getGenericTypes();
        if (generics == null || generics.size() != 1) return;
        String name = raw(generics.get(0));
        if (name != null && !name.isEmpty() && !"java.lang.Object".equals(name)) {
            names.add(name);
        }
    }

    private void auditPausedAd() throws Exception {
        List<MethodRef> requests = methodsOf(List.of(
            "kntr.app.ad.biz.videodetail.pausedpage.AdPausedPageApi$requestPausedPage$2",
            "com.bilibili.ship.theseus.united.page.pausedpage.PausedPageService$requestPausedPageData$2"
        ), method -> "invokeSuspend".equals(method.getMethodInfo().getName()) &&
            !isStatic(method) && method.getArgTypes().size() == 1);
        List<MethodRef> legacy = methodsOf(List.of("kntr.app.ad.biz.videodetail.pausedpage.ui.g"), method ->
            "invoke".equals(method.getMethodInfo().getName()) && !isStatic(method) && method.getArgTypes().isEmpty());
        List<MethodRef> panel = methodsOf(List.of("com.bilibili.ship.theseus.united.page.ad.AdPanelRepository"), method ->
            "showPanel".equals(method.getMethodInfo().getName()) && !isStatic(method) && method.getArgTypes().size() >= 2);
        feature("paused_ad", !requests.isEmpty() || !legacy.isEmpty() || !panel.isEmpty() ? "FOUND" : "MISSING",
            "request=" + refs(requests) + ";legacy=" + refs(legacy) + ";panel=" + refs(panel));
    }

    private void auditBanner() throws Exception {
        String banner = "com.bilibili.pegasus.holders.bannerv8.V8Banner";
        boolean subtype = isSubclassOf(banner, "com.bilibili.app.comm.list.widget.swiper.SwiperBanner");
        List<MethodRef> attach = methodsIncludingOwners(List.of("com.bilibili.app.comm.list.widget.swiper.SwiperBanner"), method ->
            "onAttachedToWindow".equals(method.getMethodInfo().getName()) && method.getArgTypes().isEmpty());
        feature("home_banner", subtype && !attach.isEmpty() ? "FOUND" : "MISSING",
            "subtype=" + subtype + ";attach=" + refs(attach));
    }

    private void auditDirectFeatures() throws Exception {
        boolean merchandise = !methodsOf(List.of(
            "com.bilibili.ship.theseus.united.page.intro.module.merchandise.MerchandiseComponent"
        ), method -> "createViewEntry".equals(method.getMethodInfo().getName()) &&
            args(method).equals(List.of("android.content.Context", "android.view.ViewGroup"))).isEmpty();
        feature("merchandise", merchandise ? "FOUND" : "MISSING", Boolean.toString(merchandise));

        boolean mentionBody = hasNoArgMethod("com.bapis.bilibili.app.viewunite.common.Mention", "getCardsList") ||
            hasNoArgMethod("com.bilibili.biligame.videocard.GameVideoMentionCardData", "hidden") ||
            hasNoArgMethod("com.bilibili.playerbizcommonv2.videomentioned.MentionedSectionItem", "getCards");
        boolean mentionHeader = hasNoArgMethod("com.bapis.bilibili.app.viewunite.common.Mention", "getTitle") ||
            hasNoArgMethod("com.bapis.bilibili.app.viewunite.common.VideoMentions", "getTitle") ||
            hasNoArgMethod("com.bilibili.playerbizcommonv2.videomentioned.MentionedSectionItem", "getHeader");
        feature("game_promotion", mentionBody && mentionHeader ? "FOUND" :
            (mentionBody || mentionHeader ? "PARTIAL" : "MISSING"),
            "body=" + mentionBody + ";header=" + mentionHeader);
    }

    private List<MethodRef> discoverQualityMethods(Collection<String> owners) {
        List<MethodRef> matches = new ArrayList<>();
        Collection<ClassNode> targets = exhaustiveQuality
            ? allClasses
            : owners.stream().map(classes::get).filter(java.util.Objects::nonNull).toList();
        for (ClassNode owner : targets) {
            for (MethodNode method : owner.getMethods()) {
                if (!method.getArgTypes().isEmpty() || !INT.equals(typeName(method.getReturnType())) ||
                    method.getCodeReader() == null) {
                    continue;
                }
                boolean[] hit = {false};
                method.getCodeReader().visitInstructions(instruction -> {
                    if (hit[0]) return;
                    try {
                        instruction.decode();
                        if (instruction.getOpcode() == Opcode.CONST_STRING) {
                            String value = instruction.getIndexAsString();
                            hit[0] = value != null &&
                                (value.contains("quality settings:") ||
                                    value.contains("pref_player_mediaSource_quality_wifi_key"));
                        }
                    } catch (RuntimeException ignored) {
                        // One malformed instruction must not invalidate the APK audit.
                    }
                });
                if (hit[0]) {
                    matches.add(new MethodRef(rawName(owner), method.getMethodInfo().getShortId()));
                }
            }
        }
        return matches;
    }

    private List<MethodRef> discoverMethods(Predicate<MethodNode> predicate) {
        List<MethodRef> matches = new ArrayList<>();
        for (ClassNode owner : allClasses) {
            for (MethodNode method : owner.getMethods()) {
                if (predicate.test(method)) {
                    matches.add(new MethodRef(rawName(owner), method.getMethodInfo().getShortId()));
                }
            }
        }
        return matches;
    }

    private List<MethodRef> methodsOf(Collection<String> owners, Predicate<MethodNode> predicate) {
        List<MethodRef> matches = new ArrayList<>();
        for (String owner : owners) {
            for (MethodNode method : declaredMethods(owner)) {
                if (predicate.test(method)) {
                    matches.add(new MethodRef(owner, method.getMethodInfo().getShortId()));
                }
            }
        }
        return matches;
    }

    private List<MethodRef> methodsIncludingOwners(
        Collection<String> owners,
        Predicate<MethodNode> predicate
    ) {
        List<MethodRef> matches = new ArrayList<>();
        for (String owner : owners) {
            for (MethodNode method : methodsIncludingSupers(owner)) {
                if (predicate.test(method)) {
                    matches.add(new MethodRef(rawName(method.getParentClass()), method.getMethodInfo().getShortId()));
                }
            }
        }
        return matches.stream().distinct().toList();
    }

    private List<MethodNode> declaredMethods(String owner) {
        ClassNode cls = classes.get(owner);
        return cls == null ? List.of() : cls.getMethods();
    }

    private List<MethodNode> methodsIncludingSupers(String owner) {
        List<MethodNode> methods = new ArrayList<>();
        Set<String> visited = new HashSet<>();
        String current = owner;
        while (current != null && visited.add(current)) {
            ClassNode cls = classes.get(current);
            if (cls == null) break;
            methods.addAll(cls.getMethods());
            current = raw(cls.getSuperClass());
        }
        return methods;
    }

    private boolean hasNoArgMethod(String owner, String name) {
        return methodsIncludingSupers(owner).stream().anyMatch(method ->
            name.equals(method.getMethodInfo().getName()) && !isStatic(method) && method.getArgTypes().isEmpty());
    }

    private boolean hasNoArgMethod(Collection<String> owners, Set<String> names) {
        return owners.stream().anyMatch(owner -> methodsIncludingSupers(owner).stream().anyMatch(method ->
            names.contains(method.getMethodInfo().getName()) && !isStatic(method) && method.getArgTypes().isEmpty()));
    }

    private boolean isSubclassOf(String child, String expected) {
        if (child == null || child.isEmpty()) return false;
        ArrayDeque<String> queue = new ArrayDeque<>();
        Set<String> visited = new HashSet<>();
        queue.add(child);
        while (!queue.isEmpty()) {
            String current = queue.removeFirst();
            if (!visited.add(current)) continue;
            if (expected.equals(current)) return true;
            if (VIEW.equals(expected) &&
                (current.startsWith("android.view.") || current.startsWith("android.widget.") ||
                    current.startsWith("android.webkit."))) {
                return true;
            }
            if (ACTIVITY.equals(expected) && current.startsWith("android.app.") &&
                current.endsWith("Activity")) {
                return true;
            }
            ClassNode cls = classes.get(current);
            if (cls == null) continue;
            String parent = raw(cls.getSuperClass());
            if (parent != null && !parent.isEmpty()) queue.addLast(parent);
            cls.getInterfaces().stream().map(HostCompatibilityAudit::raw)
                .filter(value -> value != null && !value.isEmpty()).forEach(queue::addLast);
        }
        return false;
    }

    private boolean implementsInterface(String child, String expected) {
        return isSubclassOf(child, expected);
    }

    private ClassNode classOf(ArgType type) {
        return classes.get(raw(type));
    }

    private static boolean knownOwnerMatches(List<MethodRef> matches, Collection<String> owners) {
        return matches.stream().anyMatch(match -> owners.contains(match.owner));
    }

    private void feature(String id, String state, String detail) throws Exception {
        write("FEATURE", id, state, detail);
    }

    private void discovery(String id, List<MethodRef> matches) throws Exception {
        for (MethodRef match : matches) {
            write("DISCOVERY", id, match.owner, match.method);
        }
    }

    private static String refs(List<MethodRef> refs) {
        if (refs.isEmpty()) return "-";
        return String.join(",", refs.stream().map(ref -> ref.owner + "#" + ref.method).toList());
    }

    private static List<String> args(MethodNode method) {
        return method.getArgTypes().stream().map(HostCompatibilityAudit::typeName).toList();
    }

    private static boolean isStatic(MethodNode method) {
        return method.getAccessFlags().isStatic();
    }

    private static boolean isStatic(FieldNode field) {
        return field.getAccessFlags().isStatic();
    }

    private static boolean isAbstract(MethodNode method) {
        return method.getAccessFlags().isAbstract();
    }

    private static String rawName(ClassNode cls) {
        return cls.getClassInfo().getRawName();
    }

    private static String raw(ArgType type) {
        if (type == null) return "";
        if (type.isArray()) return raw(type.getArrayRootElement()) + "[]".repeat(type.getArrayDimension());
        if (type.isObject()) return type.getObject();
        return type.toString();
    }

    private static String typeName(ArgType type) {
        if (type == null) return "";
        if (type.isArray()) return typeName(type.getArrayRootElement()) + "[]".repeat(type.getArrayDimension());
        if (!type.isObject()) return type.toString();
        String owner = type.getObject();
        List<ArgType> generics = type.getGenericTypes();
        if (generics == null || generics.isEmpty()) return owner;
        return owner + "<" + String.join(",", generics.stream()
            .map(HostCompatibilityAudit::typeName).toList()) + ">";
    }

    private void write(String... values) throws Exception {
        for (int index = 0; index < values.length; index++) {
            if (index > 0) writer.write('\t');
            writer.write(values[index] == null ? "" : values[index]
                .replace('\t', ' ').replace('\r', ' ').replace('\n', ' '));
        }
        writer.newLine();
    }

    private record MethodRef(String owner, String method) {
    }
}
