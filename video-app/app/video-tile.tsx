import Link from 'next/link';

export default function VideoTile({
    title,
    thumbnail,
}: {
    title: string;
    thumbnail: string
}) {
    return (
        <div className="flex h-full flex-col px-3 py-3">
            <Link
                style={{ backgroundImage: `url(${thumbnail})` }}
                className="flex aspect-video max-w-lg md:max-w-sm items-end justify-start rounded-md bg-cover p-4"
                href="/"
            >
                <div className="text-white p-3">
                    {title}
                </div>
            </Link>
        </div>
    );
}