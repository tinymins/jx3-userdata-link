import sys
import os
import re
import shutil


def copytree(src, dst, symlinks=False, ignore=None):
    if os.path.isfile(src):
        if not os.path.isfile(dst):
            print("> copy: " + src + " => " + dst)
            shutil.copy2(src, dst)
            print("  copied.")
    elif os.path.isdir(src):
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                print("> copy: " + s + " => " + d)
                if os.path.isfile(d):
                    print("  skipped.")
                    continue
                if not os.path.isdir(d):
                    os.mkdir(d)
                copytree(s, d, symlinks, ignore)
            else:
                print("> copy: " + s + " => " + d)
                if os.path.isdir(d):
                    print("  skipped.")
                    continue
                if os.path.isfile(d):
                    print("  skipped.")
                    continue
                shutil.copy2(s, d)
                print("  copied.")


def modify(file, src, dst):
    text = open(file).read()
    newText = re.sub(src, dst, text)
    if newText != text:
        open(file, "w").write(newText)


def main():
    cwd = os.path.abspath(os.path.join(__file__, os.pardir))
    client = os.path.abspath(
        input(
            "Input dist jx3 zhcn/zhtw/zhcn_exp/zhcn_hd/classic_yq folder path:\n"
        ).replace('"', "")
        if len(sys.argv) == 1
        else sys.argv[1]
    )
    split_version = os.path.basename(client.lower()).split("_")
    client_lang = split_version[0]
    if client_lang == "classic":
        client_lang = "zhcn"
    client_branch = split_version[0]
    if client_branch == "zhcn":
        client_branch = "remake"
    elif client_branch == "zhtw":
        client_branch = "intl"
    client_tech_branch = split_version[0]
    if client_tech_branch == "zhcn":
        client_tech_branch = "remake"
    elif client_tech_branch == "zhtw":
        client_tech_branch = "remake"
    client_edition = split_version[0] + "_" + split_version[1]

    if cwd == client:
        input("Error: cwd should not equals with client path!")
        exit()

    if not os.path.isdir(os.path.join(client, "bin64")):
        print("Client path is: " + client)
        input('Error: client path does not contains a sub folder named "bin64"!')
        exit()

    def format_path(s):
        return os.path.abspath(
            s.format(
                cwd=cwd,
                client=client,
                lang=client_lang,
                branch=client_branch,
                tech_branch=client_tech_branch,
                edition=client_edition,
            )
        )

    # build actions
    actions = []

    for name in ["userdata"]:
        actions.append(["mkdir", "{cwd}/../%s/{edition}" % name])
        actions.append(["mklink", "{cwd}/../%s/{edition}" % name, "{client}/%s" % name])

    for name in ["goldteambid", "homeland", "homelanddir"]:
        actions.append(["mkdir", "{cwd}/../%s/{branch}" % name])
        actions.append(["mklink", "{cwd}/../%s/{branch}" % name, "{client}/%s" % name])

    for name in ["facedata", "newfacedata", "bodydata", "screenshot", "dcim"]:
        actions.append(["mkdir", "{cwd}/../%s/{tech_branch}" % name])
        actions.append(
            ["mklink", "{cwd}/../%s/{tech_branch}" % name, "{client}/%s" % name]
        )

    for name in []:
        actions.append(["mkdir", "{cwd}/../%s" % name])
        actions.append(["mklink", "{cwd}/../%s" % name, "{client}/%s" % name])

    actions.append(["mkdir", "{cwd}/../interface"])
    actions.append(["copy", "{cwd}/interface", "{cwd}/../interface"])
    actions.append(["mkdir", "{client}/interface"])

    for addon in [
        {"name": "JX", "data": True},
        {"name": "MY", "data": True},
        {"name": "LM", "data": True},
    ]:
        if addon["data"]:
            actions.append(["mkdir", "{cwd}/../interface/%s#DATA" % addon["name"]])
            actions.append(
                [
                    "mklink",
                    "{cwd}/../interface/%s#DATA" % addon["name"],
                    "{client}/interface/%s#DATA" % addon["name"],
                ]
            )

    # print actions
    print(
        "---------------------------------------------------------------------------------"
    )
    print("Client path is: " + client)
    print(
        "---------------------------------------------------------------------------------"
    )
    for action in actions:
        if action[0] == "mkdir":
            action[1] = format_path(action[1])
            print(action[0], action[1])
        elif action[0] == "mklink":
            action[1] = format_path(action[1])
            action[2] = format_path(action[2])
            print(action[0], action[1], action[2])
        elif action[0] == "copy":
            action[1] = format_path(action[1])
            action[2] = format_path(action[2])
            print(action[0], action[1], action[2])
        elif action[0] == "modify":
            action[1] = format_path(action[1])
            print(
                action[0],
                action[1],
                action[2],
                action[3],
            )

    print(
        "---------------------------------------------------------------------------------"
    )
    input("Actions will create or link folders above. Press Enter to continue...")

    # do actions
    print(
        "---------------------------------------------------------------------------------"
    )
    os.system('cd utils && ln.exe -d "%s"' % format_path("{client}/interface"))
    os.system('cd utils && ln.exe -d "%s"' % format_path("{client}/userdata"))
    for action in actions:
        print(
            "---------------------------------------------------------------------------------"
        )
        if action[0] == "mkdir":
            print(action[0], action[1])
            os.makedirs(action[1], exist_ok=True)
        elif action[0] == "mklink":
            print(action[0], action[1], action[2])
            os.system('cd utils && ln.exe -d "%s"' % action[2])
            os.system('cd utils && ln.exe -s "%s" "%s"' % (action[2], action[1]))
        elif action[0] == "copy":
            print(action[0], action[1], action[2])
            copytree(action[1], action[2])
        elif action[0] == "modify":
            print(action[0], action[1], action[2], action[3])
            modify(action[1], action[2], action[3])

    print(
        "---------------------------------------------------------------------------------"
    )
    input("Finished. Press ENTER to continue...")
    print(
        "---------------------------------------------------------------------------------"
    )


if __name__ == "__main__":
    while True:
        main()
