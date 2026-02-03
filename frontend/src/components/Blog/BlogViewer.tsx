import React from 'react';

interface BlogViewerProps {
    content: string;
    title: string;
    topic_category?: string;
}

const BlogViewer: React.FC<BlogViewerProps> = ({ content, title, topic_category }) => {
    const renderContent = () => {
        const lines = content.split('\n');

        return lines.map((line, index) => {
            const trimmed = line.trim();

            if (!trimmed) return <div key={index} className="h-4" />;

            // Handle headings
            if (trimmed.startsWith('# ')) {
                return <h1 key={index} className="text-3xl font-bold mt-8 mb-4 text-gray-900">{trimmed.substring(2)}</h1>;
            }
            if (trimmed.startsWith('## ')) {
                return <h2 key={index} className="text-2xl font-semibold mt-6 mb-3 text-gray-900">{trimmed.substring(3)}</h2>;
            }
            if (trimmed.startsWith('### ')) {
                return <h3 key={index} className="text-xl font-medium mt-4 mb-2 text-gray-900">{trimmed.substring(4)}</h3>;
            }

            // Handle list items
            if (trimmed.startsWith('- ') || trimmed.startsWith('* ')) {
                return (
                    <li key={index} className="ml-6 mb-2 text-gray-700 leading-relaxed">
                        {trimmed.substring(2)}
                    </li>
                );
            }

            // Handle numbered lists
            if (/^\d+\.\s/.test(trimmed)) {
                return (
                    <li key={index} className="ml-6 mb-2 text-gray-700 leading-relaxed list-decimal">
                        {trimmed.replace(/^\d+\.\s/, '')}
                    </li>
                );
            }

            // Handle code blocks
            if (trimmed.startsWith('```')) {
                return null; // Handle code blocks separately if needed
            }

            // Regular paragraphs
            return (
                <p key={index} className="mb-4 text-gray-700 leading-relaxed">
                    {trimmed}
                </p>
            );
        });
    };

    return (
        <div className={`prose prose-lg max-w-none ${topic_category ? `blog-${topic_category}` : ''}`}>
            {renderContent()}
        </div>
    );
};

export default BlogViewer;
